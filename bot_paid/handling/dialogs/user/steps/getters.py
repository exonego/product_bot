import logging

from typing import TYPE_CHECKING

from aiogram.enums import ContentType
from aiogram_dialog import DialogManager
from aiogram_dialog.api.entities import MediaAttachment, MediaId
from fluentogram import TranslatorRunner

if TYPE_CHECKING:
    from I18N.locales.stub import TranslatorRunner  # type: ignore

logger = logging.getLogger(__name__)


async def step1_getter(
    dialog_manager: DialogManager, i18n: TranslatorRunner, file_ids: dict[str], **kwargs
) -> dict[str, str | MediaAttachment]:
    step1_media = MediaAttachment(
        type=ContentType.VIDEO, file_id=MediaId(file_ids.get("step1_media"))
    )

    return {
        "paiduser_steps_step1_text_p1": i18n.paiduser.steps.step1.text.p1(),
        "paiduser_steps_step1_button": i18n.paiduser.steps.step1.button(),
        "step1_media": step1_media,
    }


async def step2_getter(
    dialog_manager: DialogManager, i18n: TranslatorRunner, file_ids: dict[str], **kwargs
) -> dict[str, str | MediaAttachment]:
    step2_media = MediaAttachment(
        type=ContentType.VIDEO, file_id=MediaId(file_ids.get("step2_media"))
    )

    return {
        "paiduser_steps_step2_text_p1": i18n.paiduser.steps.step2.text.p1(),
        "paiduser_steps_step2_button": i18n.paiduser.steps.step2.button(),
        "admin_button_back": i18n.admin.button.back(),
        "step2_media": step2_media,
    }


async def step3_getter(
    dialog_manager: DialogManager, i18n: TranslatorRunner, file_ids: dict[str], **kwargs
) -> dict[str, str | MediaAttachment]:
    step3_media = MediaAttachment(
        type=ContentType.VIDEO, file_id=MediaId(file_ids.get("step3_media"))
    )

    return {
        "paiduser_steps_step3_text_p1": i18n.paiduser.steps.step3.text.p1(),
        "paiduser_steps_step3_button": i18n.paiduser.steps.step3.button(),
        "admin_button_back": i18n.admin.button.back(),
        "step3_media": step3_media,
    }


async def step4_getter(
    dialog_manager: DialogManager, i18n: TranslatorRunner, file_ids: dict[str], **kwargs
) -> dict[str, str | MediaAttachment]:
    step4_media = MediaAttachment(
        type=ContentType.VIDEO, file_id=MediaId(file_ids.get("step4_media"))
    )

    return {
        "paiduser_steps_step4_text_p1": i18n.paiduser.steps.step4.text.p1(),
        "paiduser_steps_step4_button": i18n.paiduser.steps.step4.button(),
        "admin_button_back": i18n.admin.button.back(),
        "step4_media": step4_media,
    }


async def step5_getter(
    dialog_manager: DialogManager, i18n: TranslatorRunner, file_ids: dict[str], **kwargs
) -> dict[str, str | MediaAttachment]:
    step5_media = MediaAttachment(
        type=ContentType.VIDEO, file_id=MediaId(file_ids.get("step5_media"))
    )

    return {
        "paiduser_steps_step5_text_p1": i18n.paiduser.steps.step5.text.p1(),
        "paiduser_steps_step5_button": i18n.paiduser.steps.step5.button(),
        "admin_button_back": i18n.admin.button.back(),
        "step5_media": step5_media,
    }


async def step6_getter(
    dialog_manager: DialogManager, i18n: TranslatorRunner, file_ids: dict[str], **kwargs
) -> dict[str, str]:

    return {
        "paiduser_steps_step6_text_p4": i18n.paiduser.steps.step6.text.p4(),
        "paiduser_steps_step6_button": i18n.paiduser.steps.step6.button(),
        "admin_button_back": i18n.admin.button.back(),
    }


async def step7_getter(
    dialog_manager: DialogManager, i18n: TranslatorRunner, file_ids: dict[str], **kwargs
) -> dict[str, str]:

    return {
        "paiduser_steps_step7_text_p2": i18n.paiduser.steps.step7.text.p2(),
        "admin_button_back": i18n.admin.button.back(),
    }
