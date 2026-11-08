import logging
from datetime import datetime

from sqlalchemy import select, func, and_
from sqlalchemy.ext.asyncio import AsyncSession

from database import Action

logger = logging.getLogger(__name__)


async def count_first_starts(
    session: AsyncSession, left: datetime, right: datetime
) -> int:
    """Counts the number of first starts for a period."""
    stmt = select(func.count(Action.id)).where(
        and_(
            Action.action == "first_start",
            Action.created_at > left,
            Action.created_at < right,
        )
    )
    result = await session.execute(stmt)

    return result.scalar()


async def count_buys(session: AsyncSession, left: datetime, right: datetime) -> int:
    """Counts the number of buys for a period."""
    stmt = select(func.count(Action.id)).where(
        and_(
            Action.action == "buy",
            Action.created_at > left,
            Action.created_at < right,
        )
    )
    result = await session.execute(stmt)

    return result.scalar()


async def add_first_start(session: AsyncSession, user_id: int) -> None:
    """Adds new first_start action."""
    new_action = Action(action="first_start", user_id=user_id)

    session.add(new_action)
    await session.commit()


async def add_buy(session: AsyncSession, user_id: int) -> None:
    """Adds new buy action."""
    new_action = Action(action="buy", user_id=user_id)

    session.add(new_action)
    await session.commit()
