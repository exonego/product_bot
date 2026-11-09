import logging
from decimal import Decimal

from aiogram.types import Message, CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Button, SwitchTo
from aiogram_dialog.widgets.input import ManagedTextInput
from redis.asyncio import Redis

from utils.price import set_price

logger = logging.getLogger(__name__)


async def back_to_start_handler(
    callback: CallbackQuery, button: Button, dialog_manager: DialogManager
) -> None:
    await dialog_manager.done()


async def correct_price_handler(
    message: Message, widget: ManagedTextInput, dialog_manager: DialogManager, text: str
) -> None:
    redis: Redis = dialog_manager.middleware_data.get("redis")
    product: str = dialog_manager.dialog_data.get("product")

    dialog_manager.dialog_data["price"] = text
    price = Decimal(text)
    await set_price(redis=redis, price=price)

    await dialog_manager.done()
