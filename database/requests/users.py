import logging

from sqlalchemy import select, func, and_
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from database import User
from bot.enums import Role

logger = logging.getLogger(__name__)


async def get_user(session: AsyncSession, tg_id: int) -> User:
    """Returns User by tg_id"""
    return await session.get(User, tg_id)


async def add_user(
    session: AsyncSession,
    tg_id: int,
    language: str,
    role: Role = Role.USER,
) -> None:
    """Добавляет пользователя в базу данных"""
    stmt = (
        insert(User)
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
    user = await session.get(User, tg_id)
    user.role = role
    await session.commit()


async def set_banned(session: AsyncSession, tg_id: int, banned: bool) -> None:
    """Sets banned for User"""
    user = await session.get(User, tg_id)
    user.banned = banned
    await session.commit()


async def set_is_alive(session: AsyncSession, tg_id: int, is_alive: bool) -> None:
    """Sets is_alive for User"""
    user = await session.get(User, tg_id)
    user.is_alive = is_alive
    await session.commit()


async def count_users(session: AsyncSession) -> int:
    """Counts the number of users"""
    stmt = select(func.count(User.tg_id)).where(User.role == Role.USER)
    result = await session.execute(stmt)

    return result.scalar()


async def count_alive(session: AsyncSession) -> int:
    """Возвращает количество 'живых' пользователей"""
    stmt = select(func.count(User.tg_id)).where(
        and_(User.role == Role.USER, User.is_alive == True, User.banned == False)
    )
    result = await session.execute(stmt)

    return result.scalar()
