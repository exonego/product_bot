import logging
from collections.abc import Callable, Awaitable
from typing import Any

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, User, Chat
from aiogram.enums import ChatType

logger = logging.getLogger(__name__)


class OnlyPrivateMiddleware(BaseMiddleware):
    """Middleware which ignores user's actions not from private chats"""

    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:

        user: User = data.get("event_from_user")
        if user is None:
            return await handler(event, data)

        chat: Chat = data.get("event_chat")

        if chat and chat.type != ChatType.PRIVATE:
            return

        return await handler(event, data)
