import logging

from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart
from aiogram_dialog import DialogManager, StartMode
from sqlalchemy.ext.asyncio import AsyncSession
from nats.js import JetStreamContext

from bot.enums import Role
from bot.handling.states import UserMenuSG, AdminMenuSG
from database import Requests, User
from services.delayed_service.create_delayed_dispatch import create_delayed_dispatch

logger = logging.getLogger(__name__)

requests = Requests()
start_router = Router()


@start_router.message(CommandStart())
async def command_start(
    message: Message,
    dialog_manager: DialogManager,
    session: AsyncSession,
    js: JetStreamContext,
    db_user: User | None,
    role: Role,
    subject_delayed: str,
    stream_delayed: str,
) -> None:
    """Handles /start command"""

    if db_user is None:
        await requests.users.add_user(
            session=session,
            tg_id=message.from_user.id,
            language=message.from_user.language_code,
            role=role,
        )
        if role == Role.USER:
            await requests.actions.add_first_start(
                session=session, user_id=message.from_user.id
            )

            await create_delayed_dispatch(
                js=js,
                user_id=message.from_user.id,
                message_code=1,
                delay=86400,
                subject=subject_delayed,
                stream=stream_delayed,
            )
            await create_delayed_dispatch(
                js=js,
                user_id=message.from_user.id,
                message_code=2,
                delay=86400 * 2,
                subject=subject_delayed,
                stream=stream_delayed,
            )

    else:
        await requests.users.set_is_alive(
            session=session, tg_id=message.from_user.id, is_alive=True
        )

    if role == Role.USER:
        await dialog_manager.start(
            state=UserMenuSG.window1,
            mode=StartMode.RESET_STACK,
        )
    else:
        await dialog_manager.start(state=AdminMenuSG.menu, mode=StartMode.RESET_STACK)
