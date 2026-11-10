import logging
from datetime import datetime
from typing import TYPE_CHECKING

from aiogram_dialog import DialogManager
from fluentogram import TranslatorRunner
from sqlalchemy.ext.asyncio import AsyncSession

from database import Requests

if TYPE_CHECKING:
    from I18N.locales.stub import TranslatorRunner  # type: ignore

logger = logging.getLogger(__name__)

requests = Requests()


async def general_getter(
    dialog_manager: DialogManager,
    i18n: TranslatorRunner,
    session: AsyncSession,
    **kwargs
) -> dict[str, str]:
    users = await requests.users.count_users(session=session)
    paid = await requests.paid_users.count_users(session=session)
    alive = await requests.users.count_alive(session=session)
    dead = users - alive

    return {
        "admin_metrics_general_text": i18n.admin.metrics.general.text(
            users=users, paid=paid, alive=alive, dead=dead
        ),
        "admin_metrics_general_button": i18n.admin.metrics.general.button(),
        "admin_button_back": i18n.admin.button.back(),
    }


async def sendleft_getter(
    dialog_manager: DialogManager, i18n: TranslatorRunner, **kwargs
) -> dict[str, str]:
    return {
        "admin_metrics_sendleft_text": i18n.admin.metrics.sendleft.text(),
        "admin_button_back": i18n.admin.button.back(),
    }


async def sendright_getter(
    dialog_manager: DialogManager, i18n: TranslatorRunner, **kwargs
) -> dict[str, str]:
    return {
        "admin_metrics_sendright_text": i18n.admin.metrics.sendright.text(),
        "admin_button_back": i18n.admin.button.back(),
    }


async def period_getter(
    dialog_manager: DialogManager,
    i18n: TranslatorRunner,
    session: AsyncSession,
    **kwargs
) -> dict[str, str]:
    left_str: str = dialog_manager.dialog_data.get("period_left")
    right_str: str = dialog_manager.dialog_data.get("period_right")

    left = datetime.strptime(left_str, "%d.%m.%Y")
    right = datetime.strptime(right_str, "%d.%m.%Y")
    first_starts = await requests.actions.count_first_starts(
        session=session, left=left, right=right
    )
    buys = await requests.actions.count_buys(session=session, left=left, right=right)

    return {
        "admin_metrics_period_text": i18n.admin.metrics.period.text(
            left=left_str, right=right_str, first_starts=first_starts, buys=buys
        ),
        "admin_button_back": i18n.admin.button.back(),
    }
