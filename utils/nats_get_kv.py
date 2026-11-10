import logging

from nats.js import JetStreamContext
from nats.js.kv import KeyValue
from nats.js.api import KeyValueConfig, StorageType

logger = logging.getLogger(__name__)


async def get_mailing_kv(
    js: JetStreamContext, bucket_name: str = "mailing_metadata"
) -> KeyValue:
    """Creates a KV bucket if it doesn't exist and returns the KeyValue object."""

    try:
        kv = await js.create_key_value(
            config=KeyValueConfig(
                bucket=bucket_name, history=1, storage=StorageType.FILE
            )
        )
        logger.info(f"KV Bucket '{bucket_name}' is ready.")
        return kv
    except Exception as e:
        logger.warning(f"Failed to setup KV Bucket '{bucket_name}': {e}")
        logger.info(f"Try to get KV Bucket '{bucket_name}' from Nats...")
        return await js.key_value(bucket=bucket_name)
