import logging
import asyncio
from typing import TYPE_CHECKING

from aiogram import Bot, Router, F
from aiogram.types import Message, PreCheckoutQuery
from aiogram.enums import ContentType
from sqlalchemy.ext.asyncio import AsyncSession
from fluentogram import TranslatorRunner

from database import Requests, User

if TYPE_CHECKING:
    from I18N.locales.stub import TranslatorRunner  # type: ignore

logger = logging.getLogger(__name__)

requests = Requests()
payment_router = Router()


@payment_router.pre_checkout_query()
async def process_pre_checkout_query(
    pre_checkout_query: PreCheckoutQuery, bot: Bot
) -> None:
    try:
        await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)
        logging.info(f"PreCheckout {pre_checkout_query.id} confirmed")
    except Exception as e:
        logging.error(f"Ошибка в PreCheckout: {e}")


@payment_router.message(F.content_type == ContentType.SUCCESSFUL_PAYMENT)
async def process_succesful_payment(
    message: Message,
    bot: Bot,
    session: AsyncSession,
    i18n: TranslatorRunner,
    db_user: User,
    admin_ids: list[int],
):
    if message.successful_payment.invoice_payload == "product":
        await requests.actions.add_buy(session=session, user_id=message.from_user.id)
        await requests.paid_users.add_user(
            session=session,
            tg_id=db_user.tg_id,
            language=db_user.language,
            role=db_user.role,
        )

        await message.answer(text=i18n.user.buy())

        # Notify admins
        for admin_id in admin_ids:
            await bot.send_message(
                chat_id=admin_id,
                text=i18n.admin.notify.buy(
                    username=(
                        f"@{message.from_user.username}"
                        if message.from_user.username is not None
                        else "no"
                    ),
                    user_id=str(message.from_user.id),
                ),
            )

            await asyncio.sleep(0.1)
