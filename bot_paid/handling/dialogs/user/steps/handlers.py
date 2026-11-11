import logging
from typing import TYPE_CHECKING

from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager, ShowMode
from aiogram_dialog.widgets.kbd import Button
from fluentogram import TranslatorRunner

if TYPE_CHECKING:
    from I18N.locales.stub import TranslatorRunner  # type: ignore

logger = logging.getLogger(__name__)


async def to_step6_handler(
    callback: CallbackQuery, button: Button, dialog_manager: DialogManager
) -> None:
    i18n: TranslatorRunner = dialog_manager.middleware_data.get("i18n")
    file_ids: dict[str, str] = dialog_manager.middleware_data.get("file_ids")

    await callback.message.answer_video(
        video=file_ids.get("step6_media"), caption=i18n.paiduser.steps.step6.text.p1()
    )
    await callback.message.answer(i18n.paiduser.steps.step6.text.p2())
    await callback.message.answer(i18n.paiduser.steps.step6.text.p3())

    if button.widget_id.split("_")[0] == "next":
        await dialog_manager.next(show_mode=ShowMode.SEND)
    else:
        await dialog_manager.back(show_mode=ShowMode.SEND)


async def to_step7_handler(
    callback: CallbackQuery, button: Button, dialog_manager: DialogManager
) -> None:
    i18n: TranslatorRunner = dialog_manager.middleware_data.get("i18n")
    file_ids: dict[str, str] = dialog_manager.middleware_data.get("file_ids")

    await callback.message.answer_video(
        video=file_ids.get("step7_media"), caption=i18n.paiduser.steps.step7.text.p1()
    )

    await dialog_manager.next(show_mode=ShowMode.SEND)
