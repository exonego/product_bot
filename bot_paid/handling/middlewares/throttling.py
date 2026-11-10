import logging
from collections.abc import Callable, Awaitable
from typing import Any, TYPE_CHECKING
from cachetools import TTLCache
from datetime import datetime, timedelta

from aiogram import BaseMiddleware
from aiogram.types import Update, User
from fluentogram import TranslatorRunner
from sqlalchemy.ext.asyncio import AsyncSession

from database import Requests

if TYPE_CHECKING:
    from I18N.locales.stub import TranslatorRunner  # type: ignore

logger = logging.getLogger(__name__)
requests = Requests()


class ThrottlingMiddleware(BaseMiddleware):
    def __init__(self, limit: int = 5, window: int = 5, warned_window: int = 60):
        self.cache = TTLCache(maxsize=10_000, ttl=window)
        self.warned = TTLCache(maxsize=10_000, ttl=warned_window)
        self.limit = limit
        self.window = window

    async def __call__(
        self,
        handler: Callable[[Update, dict[str, Any]], Awaitable[Any]],
        event: Update,
        data: dict[str, Any],
    ) -> Any:

        user: User = data.get("event_from_user")
        if user is None:
            return await handler(event, data)

        now = datetime.now()

        user_history = self.cache.get(user.id, [])
        user_history = [
            dt for dt in user_history if now - dt <= timedelta(seconds=self.window)
        ]
        user_history.append(now)
        self.cache[user.id] = user_history

        # if user is spammer
        if len(user_history) > self.limit:
            i18n: TranslatorRunner = data.get("i18n")

            # if user has warned
            if user.id in self.warned.keys():
                # 1. Ban him
                session: AsyncSession = data.get("session")
                await requests.users.set_banned(
                    session=session, tg_id=user.id, banned=True
                )

                # 2. Let him know
                if event.message:
                    await event.message.answer(text=i18n.user.spam.notify())
                elif event.callback_query:
                    await event.callback_query.answer(
                        text=i18n.user.spam.notify(),
                        show_alert=True,
                    )

                return

            # if user has not warned
            # 1. add him into the warned dict and clear cache
            self.warned[user.id] = True
            self.cache[user.id] = []

            # 2. warn him
            if event.message:
                await event.message.answer(text=i18n.user.spam.warning())
            elif event.callback_query:
                await event.callback_query.answer(
                    text=i18n.user.spam.warning(), show_alert=True
                )

        return await handler(event, data)
