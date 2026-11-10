import logging
import asyncio

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.fsm.storage.base import DefaultKeyBuilder
from aiogram_dialog import setup_dialogs
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from bot.handling.handlers.start_command import start_router
from bot.handling.handlers.blocked import blocked_router
from bot.handling.handlers.mailing import mailing_router
from bot.handling.handlers.user import user_router
from bot.handling.dialogs import dialog_admin_router, dialog_user_router
from bot.handling.middlewares import (
    OnlyPrivateMiddleware,
    DbSessionMiddleware,
    ShadowBanMiddleware,
    TranslatorRunnerMiddleware,
    ThrottlingMiddleware,
    RoleMiddleware,
)
from config.config import Config
from I18N import i18n_factory
from utils.load_assets import upload_assets
from utils.nats_connect import connect_to_nats
from utils.nats_setup_streams import setup_mailing_streams
from utils.nats_get_kv import get_mailing_kv
from utils.nats_start_consumers import (
    start_delayed_consumer,
    start_mailing_splitter,
    start_delivery_consumer,
)

# Module logger init
logger = logging.getLogger(__name__)


# Function for config and launch bot
async def main(config: Config) -> None:
    logger.info("Starting bot...")

    # Init redis storage
    logger.info("Init redis storage...")
    redis = Redis(
        host=config.redis.host,
        port=config.redis.port,
        db=config.redis.db,
        username=config.redis.username,
        password=config.redis.password.get_secret_value(),
    )
    storage = RedisStorage(
        redis=redis,
        key_builder=DefaultKeyBuilder(with_destiny=True),
    )

    # Create sqlalchemy engine to connect db
    logger.info("Creation sqlalchemy engine...")
    engine = create_async_engine(url=str(config.db.dsn))
    # Create sqlalchemy Sessionmaker
    logger.info("Creation sqlalchemy Sessionmaker...")
    Sessionmaker = async_sessionmaker(engine, expire_on_commit=False)

    # Connect Nats
    logger.info("Connecting Nats...")
    nc, js = await connect_to_nats(servers=config.nats.servers)
    # Setup mailing streams
    logger.info("Setting up NATS streams...")
    await setup_mailing_streams(
        js=js,
        stream_delayed=config.nats.stream_delayed,
        stream_splitter=config.nats.stream_splitter,
        stream_delivery=config.nats.stream_delivery,
        subjects_delayed=[config.nats.subject_delayed],
        subjects_splitter=[config.nats.subject_splitter],
        subjects_delivery=[config.nats.subject_delivery],
    )
    # Get mailing kv-storage
    logger.info("Getting mailing kv-storage...")
    mailing_kv = await get_mailing_kv(js=js, bucket_name=config.nats.bucket_mailing)

    # Create object type TranslatorHub
    logger.info("Creation translator_hub...")
    translator_hub = i18n_factory()

    # Init Bot and Dispatcher
    logger.info("Init bot and dispatcher...")
    tg_bot = Bot(
        token=config.bot.token.get_secret_value(),
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    dp = Dispatcher(storage=storage)

    # Setup dialogs
    logger.info("Setting up dialogs...")
    setup_dialogs(dp)

    # Include routers
    logger.info("Including routers into dispatcher...")
    dp.include_routers(
        start_router,
        blocked_router,
        user_router,
        dialog_admin_router,
        mailing_router,
        dialog_user_router,
    )

    # Register middlewares
    logger.info("Registration middlewares...")
    dp.update.outer_middleware(OnlyPrivateMiddleware())
    dp.update.outer_middleware(DbSessionMiddleware(session_pool=Sessionmaker))
    dp.update.outer_middleware(ShadowBanMiddleware())
    dp.update.outer_middleware(
        TranslatorRunnerMiddleware(translator_hub=translator_hub)
    )
    dp.update.outer_middleware(
        ThrottlingMiddleware(limit=5, window=3, warned_window=300)
    )
    dp.update.outer_middleware(RoleMiddleware())

    # Upload assets
    file_ids = await upload_assets(
        redis=redis, bot=tg_bot, chat_id=config.bot.assets_chat_id
    )

    # Start
    try:
        await asyncio.gather(
            dp.start_polling(
                tg_bot,
                admin_ids=config.bot.admin_ids,
                yoo_token=config.yoo.token,
                file_ids=file_ids,
                redis=redis,
                js=js,
                mailing_kv=mailing_kv,
                subject_delayed=config.nats.subject_delayed,
                stream_delayed=config.nats.stream_delayed,
                subject_splitter=config.nats.subject_splitter,
                stream_splitter=config.nats.stream_splitter,
            ),
            start_delayed_consumer(
                js=js,
                bot=tg_bot,
                translator_hub=translator_hub,
                Sessionmaker=Sessionmaker,
                file_ids=file_ids,
                subject=config.nats.subject_delayed,
                stream=config.nats.stream_delayed,
            ),
            start_mailing_splitter(
                js=js,
                kv=mailing_kv,
                Sessionmaker=Sessionmaker,
                subject=config.nats.subject_splitter,
                stream=config.nats.stream_splitter,
                delivery_subject=config.nats.subject_delivery,
                delivery_stream=config.nats.stream_delivery,
            ),
            start_delivery_consumer(
                js=js,
                kv=mailing_kv,
                bot=tg_bot,
                admin_ids=config.bot.admin_ids,
                translator_hub=translator_hub,
                subject=config.nats.subject_delivery,
                stream=config.nats.stream_delivery,
            ),
        )
    except Exception as e:
        logger.exception(e)
    finally:
        await nc.close()
        logger.info("Connection to Nats closed.")
        await engine.dispose()
        logger.info("PostgreSQL engine disposed.")
