import logging

from sqlalchemy import select, func, and_
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from database import PaidUser
from bot.enums import Role

logger = logging.getLogger(__name__)


async def get_user(session: AsyncSession, tg_id: int) -> PaidUser:
    """Returns User by tg_id"""
    return await session.get(PaidUser, tg_id)


async def add_user(
    session: AsyncSession,
    tg_id: int,
    language: str,
    role: Role = Role.USER,
) -> None:
    """Добавляет пользователя в базу данных"""
    stmt = (
        insert(PaidUser)
        .values(
            tg_id=tg_id,
            role=role,
            language=language,
        )
        .on_conflict_do_nothing()
    )
    await session.execute(stmt)
    await session.commit()


async def set_role(
    session: AsyncSession,
    tg_id: int,
    role: Role,
) -> None:
    """Sets role for User"""
    user = await session.get(PaidUser, tg_id)
    user.role = role
    await session.commit()


async def set_banned(session: AsyncSession, tg_id: int, banned: bool) -> None:
    """Sets banned for User"""
    user = await session.get(PaidUser, tg_id)
    user.banned = banned
    await session.commit()


async def set_is_alive(session: AsyncSession, tg_id: int, is_alive: bool) -> None:
    """Sets is_alive for User"""
    user = await session.get(PaidUser, tg_id)
    user.is_alive = is_alive
    await session.commit()
