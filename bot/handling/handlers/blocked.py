import logging

from aiogram import Router
from aiogram.types import ChatMemberUpdated
from aiogram.filters import ChatMemberUpdatedFilter, KICKED
from sqlalchemy.ext.asyncio import AsyncSession

from database import Requests
from bot.enums import Role

logger = logging.getLogger(__name__)

requests = Requests()
blocked_router = Router()


@blocked_router.my_chat_member(ChatMemberUpdatedFilter(member_status_changed=KICKED))
async def process_bot_blocked(
    event: ChatMemberUpdated, session: AsyncSession, role: Role
) -> None:
    await requests.users.set_is_alive(
        session=session, tg_id=event.from_user.id, is_alive=False
    )
    if role == Role.USER:
        await requests.actions.add_bot_block(
            session=session, user_id=event.from_user.id
        )
    logger.info(f"User {event.from_user.id} blocked the bot")
