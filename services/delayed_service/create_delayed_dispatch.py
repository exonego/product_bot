from typing import Literal
from datetime import datetime

from nats.js import JetStreamContext


async def create_delayed_dispatch(
    js: JetStreamContext,
    user_id: int,
    message_code: Literal[1, 2, 3],
    delay: int = 0,
    subject: str = "delayed.dispatch",
    stream: str = "DELAYED_DISPATCH",
) -> None:
    if message_code not in {1, 2, 3}:
        raise ValueError("message_code must be exactly an integer 1, 2, or 3")

    headers = {
        "Delayed-User-ID": str(user_id),
        "Delayed-Message-Code": str(message_code),
        "Delayed-Timestamp": str(datetime.now().timestamp()),
        "Delayed-Delay": str(delay),
    }

    await js.publish(subject=subject, stream=stream, headers=headers)
