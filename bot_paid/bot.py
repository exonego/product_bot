import logging
import asyncio

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.fsm.storage.base import DefaultKeyBuilder
from aiogram_dialog import setup_dialogs
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import async_sessionmaker
from fluentogram import TranslatorHub

from bot_paid.handling.handlers.start_command import start_router
from bot_paid.handling.handlers.blocked import blocked_router
from bot_paid.handling.dialogs import dialog_user_router
from bot_paid.handling.middlewares import (
    OnlyPrivateMiddleware,
    DbSessionMiddleware,
    ShadowBanMiddleware,
    TranslatorRunnerMiddleware,
    ThrottlingMiddleware,
    RoleMiddleware,
    OnlyPaidMiddleware,
)
from config.config import Config
from utils.load_assets import upload_assets

# Module logger init
logger = logging.getLogger(__name__)


# Function for config and launch paid_bot
async def start_paid_bot(
    config: Config,
    redis: Redis,
    Sessionmaker: async_sessionmaker,
    translator_hub: TranslatorHub,
) -> None:
    logger.info("Starting bot...")

    storage = RedisStorage(
        redis=redis,
        key_builder=DefaultKeyBuilder(
            prefix="paid_bot",
            with_destiny=True,
        ),
    )

    # Init Bot and Dispatcher
    logger.info("Init bot and dispatcher...")
    tg_bot = Bot(
        token=config.paid_bot.token.get_secret_value(),
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
    dp.update.outer_middleware(OnlyPaidMiddleware())

    # Upload assets
    file_ids = await upload_assets(
        redis=redis,
        bot=tg_bot,
        chat_id=config.bot.assets_chat_id,
        bot_type="paid",
    )

    # Start
    try:
        await dp.start_polling(
            tg_bot,
            admin_ids=config.bot.admin_ids,
            file_ids=file_ids,
            redis=redis,
        ),

    except Exception as e:
        logger.exception(e)
