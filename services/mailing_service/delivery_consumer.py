import logging
import json
import asyncio
from typing import Any, Literal, TYPE_CHECKING

from nats.js import JetStreamContext
from nats.js.kv import KeyValue
from nats.aio.msg import Msg
from aiogram import Bot
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.enums import ContentType
from aiogram.exceptions import TelegramRetryAfter, TelegramForbiddenError
from fluentogram import TranslatorHub, TranslatorRunner

if TYPE_CHECKING:
    from I18N.locales.stub import TranslatorRunner  # type: ignore

logger = logging.getLogger(__name__)


class DeliveryConsumer:
    def __init__(
        self,
        js: JetStreamContext,
        kv: KeyValue,
        bot: Bot,
        admin_ids: list[int],
        translator_hub: TranslatorHub,
        subject: str = "mailing.delivery",
        stream: str = "MAILING_DELIVERY",
        durable_name: str = "delivery-consumer",
    ):
        self.js = js
        self.kv = kv
        self.bot = bot
        self.admins: dict[
            int, dict[Literal["sended_25", "sended_50", "sended_75"], bool]
        ] = {
            admin_id: {
                "sended_25": False,
                "sended_50": False,
                "sended_75": False,
            }
            for admin_id in admin_ids
        }
        self.translator_hub = translator_hub
        self.subject = subject
        self.stream = stream
        self.durable_name = durable_name
        self._temporary_handled = 0
        self._is_running = False
        self._meta_cache = dict()

    async def run(self):
        self._is_running = True
        logger.info("Delivery consumer started.")

        while self._is_running:
            self.sub = await self.js.pull_subscribe(
                subject=self.subject,
                stream=self.stream,
                durable=self.durable_name,
            )

            while self._is_running:
                try:
                    mailing_id = None
                    msgs = await self.sub.fetch(batch=10, timeout=10)

                    for msg in msgs:
                        mailing_id = msg.headers.get("M-ID")
                        await self._process_delivery(msg)

                        await asyncio.sleep(0.1)  # To not be banned by Telegram

                    if mailing_id is not None:
                        await self._update_progress(mailing_id)
                        mailing_id = None

                except asyncio.TimeoutError:
                    continue
                except Exception as e:
                    if "connection closed" in str(e).lower():
                        logger.warning(f"NATS connection closed, reconnecting... {e}")
                        break
                    else:
                        logger.error(f"Error in delayed loop: {e}")
                        await asyncio.sleep(1)

    async def _process_delivery(self, msg: Msg) -> None:
        mailing_id = msg.headers.get("M-ID")
        user_id = int(msg.headers.get("User-Tg-ID"))
        user_lang = msg.headers.get("User-Language")

        meta = await self._get_meta(mailing_id)
        if not meta:
            await msg.term()
            return

        try:
            await self._send_message(user_id=user_id, user_lang=user_lang, meta=meta)

            self._temporary_handled += 1

            await msg.ack()
        except TelegramRetryAfter as e:
            await msg.nak(delay=e.retry_after)
        except TelegramForbiddenError:
            self._temporary_handled += 1

            await msg.term()
        except Exception as e:
            logger.error(f"Failed to send to {user_id}: {e}")
            await msg.nak(delay=60)

    async def _send_message(
        self, user_id: int, user_lang: str, meta: dict[str, Any]
    ) -> None:
        media_type = meta.get("media_type")
        media_id = meta.get("media_id")
        text = meta.get("text")

        i18n: TranslatorRunner = self.translator_hub.get_translator_by_locale(
            locale=user_lang
        )
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text=i18n.user.mailing.button(),
                        callback_data="to_window4_button",
                    )
                ]
            ]
        )

        if media_type == ContentType.PHOTO:
            await self.bot.send_photo(chat_id=user_id, photo=media_id)
            if text:
                await self.bot.send_message(
                    chat_id=user_id, text=text, reply_markup=keyboard
                )
        elif media_type == ContentType.VIDEO:
            await self.bot.send_video(chat_id=user_id, video=media_id)
            if text:
                await self.bot.send_message(
                    chat_id=user_id, text=text, reply_markup=keyboard
                )
        elif media_type == ContentType.VIDEO_NOTE:
            await self.bot.send_video_note(chat_id=user_id, video_note=media_id)
            if text:
                await self.bot.send_message(
                    chat_id=user_id, text=text, reply_markup=keyboard
                )
        elif text:
            await self.bot.send_message(
                chat_id=user_id, text=text, reply_markup=keyboard
            )

    async def _get_meta(self, mailing_id: str) -> dict[str, Any]:
        if mailing_id not in self._meta_cache.keys():
            entry = await self.kv.get(mailing_id)
            if not entry:
                return None
            self._meta_cache[mailing_id] = json.loads(entry.value.decode())
        return self._meta_cache[mailing_id]

    async def _update_progress(self, mailing_id: str) -> None:
        entry = await self.kv.get(mailing_id)
        if entry:
            meta = json.loads(entry.value.decode())
            meta["handled_users"] += self._temporary_handled
            self._temporary_handled = 0
            await self.kv.put(mailing_id, json.dumps(meta).encode())

            await self._notify_admins(
                handled=meta["handled_users"],
                total=meta["total_users"],
                mailing_id=mailing_id,
            )

    async def _notify_admins(
        self,
        handled: int,
        total: int,
        mailing_id: str,  # For tracking mailing by admins
    ) -> None:
        is_finished = handled >= total
        handled_percent = (handled / total) * 100 if total > 0 else 0

        for admin_id, admin_status in self.admins.items():
            if is_finished:
                await self.bot.send_message(
                    chat_id=admin_id,
                    text=f"{handled} of {total} (~{handled_percent:.2f}%) users received {mailing_id} mailing.\n"
                    "Status: <u>COMPLETED</u>",
                )
                self.admins[admin_id] = {
                    "sended_25": False,
                    "sended_50": False,
                    "sended_75": False,
                }
            elif handled_percent >= 75 and not admin_status["sended_75"]:
                await self.bot.send_message(
                    chat_id=admin_id,
                    text=f"{handled} of {total} (~{handled_percent:.2f}%) users received {mailing_id} mailing.\n"
                    "Status: <u>IN_PROGRESS</u>",
                )
                self.admins[admin_id]["sended_75"] = True
            elif handled_percent >= 50 and not admin_status["sended_50"]:
                await self.bot.send_message(
                    chat_id=admin_id,
                    text=f"{handled} of {total} (~{handled_percent:.2f}%) users received {mailing_id} mailing.\n"
                    "Status: <u>IN_PROGRESS</u>",
                )
                self.admins[admin_id]["sended_50"] = True
            elif handled_percent >= 25 and not admin_status["sended_25"]:
                await self.bot.send_message(
                    chat_id=admin_id,
                    text=f"{handled} of {total} (~{handled_percent:.2f}%) users received {mailing_id} mailing.\n"
                    "Status: <u>IN_PROGRESS</u>",
                )
                self.admins[admin_id]["sended_25"] = True

            await asyncio.sleep(0.1)

    def stop(self) -> None:
        self._is_running = False
