import logging
from typing import TYPE_CHECKING

from aiogram_dialog import DialogManager
from fluentogram import TranslatorRunner

if TYPE_CHECKING:
    from I18N.locales.stub import TranslatorRunner  # type: ignore

logger = logging.getLogger(__name__)


async def window_getter(
    dialog_manager: DialogManager, i18n: TranslatorRunner, **kwargs
) -> dict[str, str]:
    return {
        "admin_price_window_text": i18n.admin.price.window.text(),
        "admin_button_back": i18n.admin.button.back(),
    }
