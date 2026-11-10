import logging
from collections.abc import Callable, Awaitable
from typing import Any

from aiogram import BaseMiddleware
from aiogram.types import Update, User

from database import Requests, PaidUser as DBUser
from bot.enums import Role

logger = logging.getLogger(__name__)
requests = Requests()


class OnlyPaidMiddleware(BaseMiddleware):
    """
    Middleware which blocks updates from not paid user.
    """

    async def __call__(
        self,
        handler: Callable[[Update, dict[str, Any]], Awaitable[Any]],
        event: Update,
        data: dict[str, Any],
    ) -> Any:

        user: User = data.get("event_from_user")
        if user is None:
            return await handler(event, data)

        db_user: DBUser = data.get("db_user")
        role: Role = data.get("role")

        if db_user is None and role != Role.ADMIN:
            logger.info(f"Left user {user.id} tryed to message paid_bot")
            return

        return await handler(event, data)
