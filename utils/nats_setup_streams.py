import logging

from nats.js import JetStreamContext
from nats.js.api import StreamConfig, RetentionPolicy, StorageType

logger = logging.getLogger(__name__)


async def setup_mailing_streams(
    js: JetStreamContext,
    stream_delayed: str = "DELAYED_DISPATCH",
    stream_splitter: str = "MAILING_SPLITTER",
    stream_delivery: str = "MAILING_DELIVERY",
    subjects_delayed: list[str] = ["delayed.dispatch"],
    subjects_splitter: list[str] = ["mailing.splitter"],
    subjects_delivery: list[str] = ["mailing.delivery"],
) -> None:
    """Initializes Nats JetStream stream."""

    # Delayed stream
    await js.add_stream(
        config=StreamConfig(
            name=stream_delayed,
            subjects=subjects_delayed,
            retention=RetentionPolicy.LIMITS,
            storage=StorageType.FILE,
            duplicate_window=0,
            max_age=172800,
        )
    )

    # Splitter stream
    await js.add_stream(
        config=StreamConfig(
            name=stream_splitter,
            subjects=subjects_splitter,
            retention=RetentionPolicy.LIMITS,
            storage=StorageType.FILE,
            duplicate_window=0,
            max_age=3600,
        )
    )

    # Delivery stream
    await js.add_stream(
        config=StreamConfig(
            name=stream_delivery,
            subjects=subjects_delivery,
            retention=RetentionPolicy.LIMITS,
            storage=StorageType.FILE,
            duplicate_window=0,
            max_age=86400,
        )
    )

    logger.info("Nats streams initialized.")
