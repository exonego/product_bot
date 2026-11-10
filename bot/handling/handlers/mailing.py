import logging

from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager, StartMode

from bot.handling.states import UserMenuSG

logger = logging.getLogger(__name__)

mailing_router = Router()


@mailing_router.callback_query(F.data == "to_window4_button")
async def command_start(
    callback: CallbackQuery,
    dialog_manager: DialogManager,
) -> None:
    await dialog_manager.start(state=UserMenuSG.window4, mode=StartMode.RESET_STACK)
