import logging
from datetime import datetime
from typing import TYPE_CHECKING

from aiogram.types import Message, CallbackQuery
from aiogram.enums import ContentType
from aiogram_dialog import DialogManager, ShowMode
from aiogram_dialog.widgets.kbd import Button, Back, Next
from aiogram_dialog.widgets.input import ManagedTextInput, MessageInput
from fluentogram import TranslatorRunner
from sqlalchemy.ext.asyncio import AsyncSession

from database import Requests
from utils.checks import date_check

if TYPE_CHECKING:
    from I18N.locales.stub import TranslatorRunner  # type: ignore

logger = logging.getLogger(__name__)

requests = Requests()


async def back_to_start_handler(
    callback: CallbackQuery, button: Button, dialog_manager: DialogManager
) -> None:
    await dialog_manager.done()


async def sendleft_handler(
    message: Message, widget: ManagedTextInput, dialog_manager: DialogManager, text: str
) -> None:
    dialog_manager.dialog_data["period_left"] = text

    await dialog_manager.next()


async def sendright_handler(
    message: Message, widget: ManagedTextInput, dialog_manager: DialogManager, text: str
) -> None:
    period_left = dialog_manager.dialog_data.get("period_left")

    if datetime.strptime(period_left, "%d.%m.%Y") < datetime.strptime(text, "%d.%m.%Y"):
        dialog_manager.dialog_data["period_right"] = text

        await dialog_manager.next()
    else:
        i18n: TranslatorRunner = dialog_manager.dialog_data.get("i18n")

        await message.answer(text=i18n.admin.metrics.invalid.text())
