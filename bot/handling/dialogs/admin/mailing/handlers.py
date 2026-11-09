import logging
from typing import TYPE_CHECKING

from aiogram.types import (
    Message,
    CallbackQuery,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)
from aiogram.enums import ContentType
from aiogram_dialog import DialogManager, ShowMode
from aiogram_dialog.widgets.kbd import Button, Back, Next
from aiogram_dialog.widgets.input import ManagedTextInput, MessageInput
from fluentogram import TranslatorRunner
from sqlalchemy.ext.asyncio import AsyncSession
from nats.js import JetStreamContext
from nats.js.kv import KeyValue

from services.mailing_service.create_mailing_task import create_mailing_task

if TYPE_CHECKING:
    from I18N.locales.stub import TranslatorRunner  # type: ignore

logger = logging.getLogger(__name__)


async def back_to_start_handler(
    callback: CallbackQuery, button: Button, dialog_manager: DialogManager
) -> None:
    if button.widget_id == "back_to_start_from_mailing_started":
        await dialog_manager.done(show_mode=ShowMode.SEND)
    else:
        await dialog_manager.done()


async def send_text_skip_handler(
    callback: CallbackQuery, button: Next, dialog_manager: DialogManager
) -> None:
    dialog_manager.dialog_data["text_skipped"] = True


async def send_text_handler(
    message: Message, widget: ManagedTextInput, dialog_manager: DialogManager, text: str
) -> None:
    dialog_manager.dialog_data["m_text"] = text

    await dialog_manager.next()


async def back_to_send_text_handler(
    callback: CallbackQuery, button: Back, dialog_manager: DialogManager
) -> None:
    dialog_manager.dialog_data["text_skipped"] = False


async def send_media_skip_handler(
    callback: CallbackQuery, button: Back, dialog_manager: DialogManager
) -> None:
    i18n: TranslatorRunner = dialog_manager.middleware_data.get("i18n")
    m_text: str = dialog_manager.dialog_data.get("m_text")

    await callback.message.answer(text=i18n.admin.mailing.examle.text())
    await callback.message.answer(text=m_text)

    await dialog_manager.show()


async def send_media_handler(
    message: Message, widget: MessageInput, dialog_manager: DialogManager
) -> None:
    i18n: TranslatorRunner = dialog_manager.middleware_data.get("i18n")
    m_text: str = dialog_manager.dialog_data.get("m_text")

    await message.answer(text=i18n.admin.mailing.examle.text())

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=i18n.user.mailing.button(), callback_data="to_window4_button"
                )
            ]
        ]
    )

    if message.photo:
        dialog_manager.dialog_data["m_media_type"] = ContentType.PHOTO
        dialog_manager.dialog_data["m_media_id"] = message.photo[-1].file_id

        await message.answer_photo(photo=message.photo[-1].file_id)
        if m_text:
            await message.answer(text=m_text, reply_markup=keyboard)
    elif message.video:
        dialog_manager.dialog_data["m_media_type"] = ContentType.VIDEO
        if m_text:
            dialog_manager.dialog_data["m_media_id"] = message.video.file_id

        await message.answer_video(video=message.video.file_id)
        if m_text:
            await message.answer(text=m_text, reply_markup=keyboard)
    elif message.video_note:
        dialog_manager.dialog_data["m_media_type"] = ContentType.VIDEO_NOTE
        dialog_manager.dialog_data["m_media_id"] = message.video_note.file_id

        await message.answer_video_note(video_note=message.video_note.file_id)
        if m_text:
            await message.answer(text=m_text, reply_markup=keyboard)

    await dialog_manager.next()


async def confirm_mailing_handler(
    callback: CallbackQuery, button: Next, dialog_manager: DialogManager
) -> None:
    js: JetStreamContext = dialog_manager.middleware_data.get("js")
    kv: KeyValue = dialog_manager.middleware_data.get("mailing_kv")
    session: AsyncSession = dialog_manager.middleware_data.get("session")
    subject: str = dialog_manager.middleware_data.get("subject_splitter")
    stream: str = dialog_manager.middleware_data.get("stream_splitter")

    text: str = dialog_manager.dialog_data.get("m_text")
    media_id: str = dialog_manager.dialog_data.get("m_media_id")
    media_type: str = dialog_manager.dialog_data.get("m_media_type")

    mailing_id = await create_mailing_task(
        js=js,
        kv=kv,
        session=session,
        text=text,
        media_id=media_id,
        media_type=media_type,
        subject=subject,
        stream=stream,
    )

    dialog_manager.dialog_data["mailing_id"] = mailing_id
