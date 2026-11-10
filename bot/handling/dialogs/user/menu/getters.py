import logging

from typing import TYPE_CHECKING

from aiogram.enums import ContentType
from aiogram_dialog import DialogManager
from aiogram_dialog.api.entities import MediaAttachment, MediaId
from fluentogram import TranslatorRunner
from redis.asyncio import Redis

from database import Requests
from utils.price import get_price

if TYPE_CHECKING:
    from I18N.locales.stub import TranslatorRunner  # type: ignore

logger = logging.getLogger(__name__)


async def window1_getter(
    dialog_manager: DialogManager,
    i18n: TranslatorRunner,
    file_ids: dict[str, str],
    **kwargs
) -> dict[str, str | MediaAttachment]:
    media = MediaAttachment(
        type=ContentType.PHOTO, file_id=MediaId(file_ids.get("window1_media"))
    )

    return {
        "user_menu_window1_text": i18n.user.menu.window1.text(),
        "user_menu_window1_button": i18n.user.menu.window1.button(),
        "window1_media": media,
    }


async def window2_getter(
    dialog_manager: DialogManager,
    i18n: TranslatorRunner,
    file_ids: dict[str, str],
    **kwargs
) -> dict[str, str | MediaAttachment]:
    media = MediaAttachment(
        type=ContentType.PHOTO, file_id=MediaId(file_ids.get("window2_media"))
    )

    return {
        "user_menu_window2_text": i18n.user.menu.window2.text(),
        "user_menu_window2_button": i18n.user.menu.window2.button(),
        "window2_media": media,
    }


async def window3_getter(
    dialog_manager: DialogManager,
    i18n: TranslatorRunner,
    file_ids: dict[str, str],
    **kwargs
) -> dict[str, str | MediaAttachment]:
    media = MediaAttachment(
        type=ContentType.PHOTO, file_id=MediaId(file_ids.get("window3_media"))
    )

    return {
        "user_menu_window3_text": i18n.user.menu.window3.text(),
        "user_menu_window3_button": i18n.user.menu.window3.button(),
        "window3_media": media,
    }


async def window4_getter(
    dialog_manager: DialogManager,
    i18n: TranslatorRunner,
    file_ids: dict[str, str],
    redis: Redis,
    **kwargs
) -> dict[str, str | MediaAttachment]:
    media = MediaAttachment(
        type=ContentType.PHOTO, file_id=MediaId(file_ids.get("window4_media"))
    )
    price = await get_price(redis=redis)
    return {
        "user_menu_window4_text": i18n.user.menu.window4.text(),
        "user_menu_window4_button": i18n.user.menu.window4.button(price=price),
        "window4_media": media,
    }
