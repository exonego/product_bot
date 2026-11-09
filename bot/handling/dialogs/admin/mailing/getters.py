import logging
from typing import TYPE_CHECKING

from aiogram_dialog import DialogManager
from fluentogram import TranslatorRunner

if TYPE_CHECKING:
    from I18N.locales.stub import TranslatorRunner  # type: ignore

logger = logging.getLogger(__name__)


async def send_text_getter(
    dialog_manager: DialogManager, i18n: TranslatorRunner, **kwargs
) -> dict[str, str]:
    return {
        "admin_mailing_sendtext_text": i18n.admin.mailing.sendtext.text(),
        "admin_button_back": i18n.admin.button.back(),
        "admin_button_skip": i18n.admin.button.skip(),
    }


async def send_media_getter(
    dialog_manager: DialogManager, i18n: TranslatorRunner, **kwargs
) -> dict[str, str]:
    return {
        "admin_mailing_sendmedia_text": i18n.admin.mailing.sendmedia.text(),
        "admin_button_back": i18n.admin.button.back(),
        "admin_button_skip": i18n.admin.button.skip(),
        "text_not_skipped": not dialog_manager.dialog_data.get("text_skipped"),
    }


async def confirm_getter(
    dialog_manager: DialogManager, i18n: TranslatorRunner, **kwargs
) -> dict[str, str]:
    return {
        "admin_mailing_confirm_text": i18n.admin.mailing.confirm.text(),
        "admin_button_back": i18n.admin.button.back(),
        "admin_button_confirm": i18n.admin.button.confirm(),
    }


async def started_getter(
    dialog_manager: DialogManager, i18n: TranslatorRunner, **kwargs
) -> dict[str, str]:
    mailing_id = dialog_manager.dialog_data.get("mailing_id", "MAILING_ID NOT FOUND")

    return {
        "admin_mailing_started_text": i18n.admin.mailing.started.text(
            mailing_id=mailing_id
        ),
        "admin_button_back": i18n.admin.button.back(),
    }
