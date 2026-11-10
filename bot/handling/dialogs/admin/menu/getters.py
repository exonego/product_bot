import logging
from typing import TYPE_CHECKING

from aiogram_dialog import DialogManager
from fluentogram import TranslatorRunner
from redis.asyncio import Redis

from database import Requests
from utils.price import get_price

if TYPE_CHECKING:
    from I18N.locales.stub import TranslatorRunner  # type: ignore

logger = logging.getLogger(__name__)

requests = Requests()


async def start_getter(
    dialog_manager: DialogManager, i18n: TranslatorRunner, redis: Redis, **kwargs
) -> dict[str, str]:
    price = await get_price(redis=redis)

    return {
        "admin_menu_text": i18n.admin.menu.text(price=price if price else "no"),
        "admin_menu_button_metrics": i18n.admin.menu.button.metrics(),
        "admin_menu_button_mailing": i18n.admin.menu.button.mailing(),
        "admin_menu_button_price": i18n.admin.menu.button.price(),
        "admin_menu_button_leave": i18n.admin.menu.button.leave(),
    }
