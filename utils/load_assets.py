import logging
import json
from datetime import datetime

from aiogram import Bot
from aiogram.types import FSInputFile
from redis.asyncio import Redis

logger = logging.getLogger(__name__)


async def upload_assets(
    redis: Redis, bot: Bot, chat_id: int, bot_type: str
) -> dict[str, int]:
    """
    Try to get asset file_id's from redis and return they in dict
    If can't, upload assets in chat and save them file_id's
    """
    assets: dict[str, dict[str, str | int]] = {
        "window1_media": {
            "path": "/product_bot/assets/window1_media.jpg",
            "bot": "main",
        },
        "window2_media": {
            "path": "/product_bot/assets/window2_media.jpg",
            "bot": "main",
        },
        "window3_media": {
            "path": "/product_bot/assets/window3_media.jpg",
            "bot": "main",
        },
        "window4_media": {
            "path": "/product_bot/assets/window4_media.jpg",
            "bot": "main",
        },
        "delayed1_media": {
            "path": "/product_bot/assets/delayed1_media.jpg",
            "bot": "main",
        },
        "delayed2_media": {
            "path": "/product_bot/assets/delayed2_media.jpg",
            "bot": "main",
        },
        "step1_media": {
            "path": "/product_bot/assets/step1_media.MP4",
            "width": 1280,
            "height": 720,
            "bot": "paid",
        },
        "step2_media": {
            "path": "/product_bot/assets/step2_media.MP4",
            "width": 1920,
            "height": 1080,
            "bot": "paid",
        },
        "step3_media": {
            "path": "/product_bot/assets/step3_media.MP4",
            "width": 1920,
            "height": 1000,
            "bot": "paid",
        },
        "step4_media": {
            "path": "/product_bot/assets/step4_media.MP4",
            "width": 1920,
            "height": 1032,
            "bot": "paid",
        },
        "step5_media": {
            "path": "/product_bot/assets/step5_media.MP4",
            "width": 1920,
            "height": 1032,
            "bot": "paid",
        },
        "step6_media": {
            "path": "/product_bot/assets/step6_media.MP4",
            "width": 1920,
            "height": 1032,
            "bot": "paid",
        },
        "step7_media": {
            "path": "/product_bot/assets/step7_media.MP4",
            "width": 1920,
            "height": 1032,
            "bot": "paid",
        },
    }
    file_ids = dict()
    # Try to take file_id's from Redis
    result_raw = await redis.get("asset_file_ids")
    flag = True
    if result_raw:
        file_ids: dict = json.loads(result_raw)
        for key in assets.keys():
            if assets[key]["bot"] != bot_type:
                continue
            if key not in file_ids.keys():
                flag = False
        if flag:
            return file_ids

    # If can't - upload assets in chat and save them file_ids
    result = file_ids
    for key, meta in assets.items():
        if meta["bot"] != bot_type:
            continue
        logger.info(f"Uploading the {key} asset...")
        file_extension = meta.get("path").split(".")[-1].lower()

        if file_extension == "pdf":
            document = FSInputFile(path=meta.get("path"))
            message = await bot.send_document(
                chat_id=chat_id, document=document, caption=f"{key}: {datetime.now()}"
            )
            result[key] = message.document.file_id
        elif file_extension in ("jpg", "jpeg", "png"):
            photo = FSInputFile(meta.get("path"))
            message = await bot.send_photo(
                chat_id=chat_id,
                photo=photo,
                caption=f"{key}: {datetime.now()}",
                request_timeout=60,
            )
            result[key] = message.photo[-1].file_id
        elif file_extension in ["mov", "mp4"]:
            video = FSInputFile(meta.get("path"))
            message = await bot.send_video(
                chat_id=chat_id,
                video=video,
                width=meta.get("width"),
                height=meta.get("height"),
                caption=f"{key}: {datetime.now()}",
                request_timeout=1500,
            )
            result[key] = message.video.file_id

        logger.info(f"The {key} asset loaded")

    # Load file_id's in Redis
    await redis.set("asset_file_ids", json.dumps(result))

    return result
