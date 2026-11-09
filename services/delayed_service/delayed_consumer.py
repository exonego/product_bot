import logging
import asyncio
from datetime import datetime, timedelta, timezone
from typing import TYPE_CHECKING, Literal

from nats.js import JetStreamContext
from nats.aio.msg import Msg
from aiogram import Bot
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.exceptions import TelegramRetryAfter, TelegramForbiddenError
from fluentogram import TranslatorHub, TranslatorRunner
from sqlalchemy.ext.asyncio import async_sessionmaker

from database import Requests

if TYPE_CHECKING:
    from I18N.locales.stub import TranslatorRunner  # type: ignore

logger = logging.getLogger(__name__)

requests = Requests()


class DelayedConsumer:
    def __init__(
        self,
        js: JetStreamContext,
        bot: Bot,
        translator_hub: TranslatorHub,
        Sessionmaker: async_sessionmaker,
        file_ids: dict[str, str],
        subject: str = "delayed.dispatch",
        stream: str = "DELAYED_DISPATCH",
        durable_name: str = "delayed-consumer",
    ):
        self.js = js
        self.bot = bot
        self.translator_hub = translator_hub
        self.Sessionmaker = Sessionmaker
        self.file_ids = file_ids
        self.subject = subject
        self.stream = stream
        self.durable_name = durable_name

        self._is_running = False

    async def run(self):
        self._is_running = True
        logger.info("Delayed consumer started.")

        while self._is_running:
            self.sub = await self.js.pull_subscribe(
                subject=self.subject,
                stream=self.stream,
                durable=self.durable_name,
            )

            while self._is_running:
                try:
                    msgs = await self.sub.fetch(batch=10, timeout=10)
                    for msg in msgs:
                        await self._dispatch(msg)
                except asyncio.TimeoutError:
                    continue
                except Exception as e:
                    if "connection closed" in str(e).lower():
                        logger.warning(f"NATS connection closed, reconnecting... {e}")
                        break
                    else:
                        logger.error(f"Error in delayed loop: {e}")
                        await asyncio.sleep(1)

    async def _dispatch(self, msg: Msg):
        user_id = int(msg.headers.get("Delayed-User-ID"))
        sent_datetime = datetime.fromtimestamp(
            float(msg.headers.get("Delayed-Timestamp")), tz=timezone.utc
        )
        delay = int(msg.headers.get("Delayed-Delay"))

        if sent_datetime + timedelta(seconds=delay) <= datetime.now(tz=timezone.utc):
            # If that's time for handling
            async with self.Sessionmaker() as session:
                user = await requests.users.get_user(session=session, tg_id=user_id)
            if user.is_alive:
                message_code = int(msg.headers.get("Delayed-Message-Code"))
                try:
                    await self._send_message(
                        user_id=user.tg_id,
                        user_lang=user.language,
                        message_code=message_code,
                    )
                    await msg.ack()
                except TelegramRetryAfter as e:
                    await msg.nak(delay=e.retry_after)
                except TelegramForbiddenError:
                    await msg.term()
                except Exception as e:
                    logger.error(f"Failed to send to {user_id}: {e}")
                    await msg.nak(delay=60)
            else:
                # If user blocked the bot
                await msg.term()
        else:
            # If that's not time for handling then send nak with new delay
            new_delay = (
                sent_datetime + timedelta(seconds=delay) - datetime.now(tz=timezone.utc)
            ).total_seconds()

            await msg.nak(delay=new_delay)

    async def _send_message(
        self, user_id, user_lang: str, message_code: Literal[1, 2, 3]
    ) -> None:
        i18n: TranslatorRunner = self.translator_hub.get_translator_by_locale(
            locale=user_lang
        )

        if message_code == 1:
            keyboard = InlineKeyboardMarkup(
                inline_keyboard=[
                    [
                        InlineKeyboardButton(
                            text=i18n.user.delayed1.button(),
                            callback_data="to_window4_button",
                        )
                    ]
                ]
            )
            await self.bot.send_photo(
                chat_id=user_id,
                photo=self.file_ids.get("delayed1_media"),
                caption=i18n.user.delayed1.text(),
                reply_markup=keyboard,
            )
        elif message_code == 2:
            keyboard = InlineKeyboardMarkup(
                inline_keyboard=[
                    [
                        InlineKeyboardButton(
                            text=i18n.user.delayed2.button(),
                            callback_data="to_window4_button",
                        )
                    ]
                ]
            )
            await self.bot.send_photo(
                chat_id=user_id,
                photo=self.file_ids.get("delayed2_media"),
                caption=i18n.user.delayed2.text(),
                reply_markup=keyboard,
            )
