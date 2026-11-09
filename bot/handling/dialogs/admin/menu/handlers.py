import logging

from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Button

from database import Requests
from bot.handling.states import MetricsSG, PriceSG, MailingSG, UserMenuSG

logger = logging.getLogger(__name__)

requests = Requests()


async def start_metrics_handler(
    callback: CallbackQuery, button: Button, dialog_manager: DialogManager
) -> None:
    await dialog_manager.start(state=MetricsSG.endurance)


async def start_price_handler(
    callback: CallbackQuery, button: Button, dialog_manager: DialogManager
) -> None:
    await dialog_manager.start(state=PriceSG.price)


async def start_mailing_handler(
    callback: CallbackQuery, button: Button, dialog_manager: DialogManager
) -> None:
    await dialog_manager.start(state=MailingSG.send_text)


async def leave_handler(
    callback: CallbackQuery, button: Button, dialog_manager: DialogManager
) -> None:
    await dialog_manager.start(state=UserMenuSG.start)
