import logging

from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart
from aiogram_dialog import DialogManager, StartMode
from sqlalchemy.ext.asyncio import AsyncSession

from bot.enums import Role
from bot_paid.handling.states import StepsSG
from database import Requests, PaidUser

logger = logging.getLogger(__name__)

requests = Requests()
start_router = Router()


@start_router.message(CommandStart())
async def command_start(
    message: Message,
    dialog_manager: DialogManager,
    session: AsyncSession,
    db_user: PaidUser | None,
    role: Role,
) -> None:
    """Handles /start command"""

    if db_user is None:
        await requests.paid_users.add_user(
            session=session,
            tg_id=message.from_user.id,
            language=message.from_user.language_code,
            role=role,
        )
    else:
        await requests.paid_users.set_is_alive(
            session=session, tg_id=message.from_user.id, is_alive=True
        )

    await dialog_manager.start(
        state=StepsSG.step1,
        mode=StartMode.RESET_STACK,
    )
