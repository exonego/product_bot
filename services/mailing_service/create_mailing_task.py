import logging
import json
import uuid

from nats.js import JetStreamContext
from nats.js.kv import KeyValue
from sqlalchemy.ext.asyncio import AsyncSession

from database import Requests

logger = logging.getLogger(__name__)

requests = Requests()


async def create_mailing_task(
    js: JetStreamContext,
    kv: KeyValue,
    session: AsyncSession,
    text: str | None,
    media_id: str | None,
    media_type: str | None,
    subject: str = "mailing.splitter",
    stream: str = "MAILING_SPLITTER",
) -> str:
    if not text and not (media_id and media_type):
        raise ValueError("Text or media must be passed")
    elif not (media_id and media_type) and (media_type or media_id):
        raise ValueError("Not all media parameters were passed")

    # Generate unique mailing_id
    mailing_id = f"ml_{uuid.uuid4().hex[:8]}"

    # Load mailing to key-value-storage
    meta = {
        "text": text,
        "media_id": media_id,
        "media_type": media_type,
        "last_handled_tg_id": 0,
        "handled_users": 0,
        "total_users": await requests.users.get_count_for_mailing(session=session),
        "status": "IN_PROGRESS",
    }
    await kv.put(mailing_id, json.dumps(meta).encode())

    # Publish to nats
    logger.debug(f"Starting mailing {mailing_id}...")
    await js.publish(subject=subject, stream=stream, payload=mailing_id.encode())

    # Return mailing_id
    return mailing_id
