import logging
import json
from decimal import Decimal
from typing import TYPE_CHECKING

from pydantic import SecretStr
from aiogram.types import CallbackQuery, LabeledPrice
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Button
from fluentogram import TranslatorRunner
from sqlalchemy.ext.asyncio import AsyncSession
from redis.asyncio import Redis

from database import User, PaidUser, Requests
from utils.price import get_price

if TYPE_CHECKING:
    from I18N.locales.stub import TranslatorRunner  # type: ignore


logger = logging.getLogger(__name__)

requests = Requests()


async def send_invoice_handler(
    callback: CallbackQuery, button: Button, dialog_manager: DialogManager
) -> None:
    db_user: User = dialog_manager.middleware_data.get("db_user")
    i18n: TranslatorRunner = dialog_manager.middleware_data.get("i18n")
    session: AsyncSession = dialog_manager.middleware_data.get("session")

    paid_user: PaidUser = await requests.paid_users.get_user(
        session=session, tg_id=db_user.tg_id
    )

    if not paid_user:
        redis: Redis = dialog_manager.middleware_data.get("redis")

        await dialog_manager.done()

        yoo_token: SecretStr = dialog_manager.middleware_data.get("yoo_token")
        product_price: Decimal = await get_price(redis=redis)

        receipt = {
            "items": [
                {
                    "description": i18n.user.invoice.description(),
                    "amount": {
                        "value": str(product_price),
                        "currency": "RUB",
                    },
                    "vat_code": 1,
                    "quantity": 1.0,
                    "measure": "piece",
                    "payment_subject": "service",
                    "payment_mode": "full_payment",
                }
            ],
            "internet": True,
        }

        await callback.message.answer_invoice(
            title=i18n.user.invoice.title(),
            description=i18n.user.invoice.description(),
            payload="product",
            provider_token=yoo_token.get_secret_value(),
            currency="RUB",
            prices=[LabeledPrice(label="RUB", amount=int(product_price * 100))],
            need_email=True,
            send_email_to_provider=True,
            provider_data=json.dumps({"receipt": receipt}),
        )
    else:
        await callback.message.answer(text=i18n.user.paid())
