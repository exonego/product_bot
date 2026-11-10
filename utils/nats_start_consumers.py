import logging

from nats.js.client import JetStreamContext
from nats.js.kv import KeyValue
from sqlalchemy.ext.asyncio import async_sessionmaker
from fluentogram import TranslatorHub
from aiogram import Bot

from services.delayed_service.delayed_consumer import DelayedConsumer
from services.mailing_service.mailing_splitter import MailingSplitter
from services.mailing_service.delivery_consumer import DeliveryConsumer

logger = logging.getLogger(__name__)


async def start_delayed_consumer(
    js: JetStreamContext,
    bot: Bot,
    translator_hub: TranslatorHub,
    Sessionmaker: async_sessionmaker,
    file_ids: dict[str, str],
    subject: str = "delayed.dispatch",
    stream: str = "DELAYED_DISPATCH",
    durable_name: str = "delayed-consumer",
) -> None:
    """Starts delayed consumer."""

    consumer = DelayedConsumer(
        js=js,
        bot=bot,
        translator_hub=translator_hub,
        Sessionmaker=Sessionmaker,
        file_ids=file_ids,
        subject=subject,
        stream=stream,
        durable_name=durable_name,
    )
    logger.info("Starting delayed consumer...")
    await consumer.run()


async def start_mailing_splitter(
    js: JetStreamContext,
    kv: KeyValue,
    Sessionmaker: async_sessionmaker,
    subject: str = "mailing.splitter",
    stream: str = "MAILING_SPLITTER",
    delivery_subject: str = "mailing.delivery",
    delivery_stream: str = "MAILING_DELIVERY",
    durable_name: str = "splitter-consumer",
) -> None:
    """Starts mailing splitter."""

    consumer = MailingSplitter(
        js=js,
        kv=kv,
        Sessionmaker=Sessionmaker,
        subject=subject,
        stream=stream,
        delivery_subject=delivery_subject,
        delivery_stream=delivery_stream,
        durable_name=durable_name,
    )
    logger.info("Starting mailing splitter...")
    await consumer.run()


async def start_delivery_consumer(
    js: JetStreamContext,
    kv: KeyValue,
    bot: Bot,
    admin_ids: list[int],
    translator_hub: TranslatorHub,
    subject: str = "mailing.delivery",
    stream: str = "MAILING_DELIVERY",
    durable_name: str = "delivery-consumer",
) -> None:
    """Starts delivery consumer."""

    consumer = DeliveryConsumer(
        js=js,
        kv=kv,
        bot=bot,
        admin_ids=admin_ids,
        translator_hub=translator_hub,
        subject=subject,
        stream=stream,
        durable_name=durable_name,
    )
    logger.info("Starting delivery consumer...")
    await consumer.run()
