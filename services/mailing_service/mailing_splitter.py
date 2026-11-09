import logging
import json
import asyncio

from nats.js import JetStreamContext
from nats.js.kv import KeyValue
from nats.aio.msg import Msg
from sqlalchemy.ext.asyncio import async_sessionmaker

from database import Requests

logger = logging.getLogger(__name__)

requests = Requests()


class MailingSplitter:
    def __init__(
        self,
        js: JetStreamContext,
        kv: KeyValue,
        Sessionmaker: async_sessionmaker,
        subject: str = "mailing.splitter",
        stream: str = "MAILING_SPLITTER",
        delivery_subject: str = "mailing.delivery",
        delivery_stream: str = "MAILING_DELIVERY",
        durable_name: str = "splitter-consumer",
    ):
        self.js = js
        self.kv = kv
        self.Sessionmaker = Sessionmaker
        self.subject = subject
        self.stream = stream
        self.delivery_subject = delivery_subject
        self.delivery_stream = delivery_stream
        self.durable_name = durable_name
        self._is_running = False

    async def run(self):
        self._is_running = True
        logger.info("Splitter consumer started.")

        while self._is_running:
            self.sub = await self.js.pull_subscribe(
                subject=self.subject,
                stream=self.stream,
                durable=self.durable_name,
            )

            while self._is_running:
                try:
                    msgs = await self.sub.fetch(batch=1, timeout=10)
                    for msg in msgs:
                        await self._process_batch(msg)
                except asyncio.TimeoutError:
                    continue
                except Exception as e:
                    if "connection closed" in str(e).lower():
                        logger.warning(f"NATS connection closed, reconnecting... {e}")
                        break
                    else:
                        logger.error(f"Error in delayed loop: {e}")
                        await asyncio.sleep(1)

    async def _process_batch(self, msg: Msg) -> None:
        mailing_id = msg.data.decode()

        # Get current meta from KV
        entry_meta = await self.kv.get(mailing_id)
        if not entry_meta:
            logger.warning(f"No metadata found for {mailing_id}")
            await msg.ack()
            return

        meta: dict = json.loads(entry_meta.value.decode())
        last_handled_tg_id: int = meta.get("last_handled_tg_id", 0)

        # DB-Query
        async with self.Sessionmaker() as session:
            users = await requests.users.get_batch_for_mailing(
                session=session, last_handled_tg_id=last_handled_tg_id
            )

        # Check on finish
        if not users:
            await self._finish_mailing(mailing_id, meta)
            await msg.ack()
            return

        # Cut tasks for DeliveryConsumer
        for user in users:
            await self.js.publish(
                subject=self.delivery_subject,
                stream=self.delivery_stream,
                headers={
                    "M-ID": mailing_id,
                    "User-Tg-ID": str(user.tg_id),
                    "User-Language": user.language,
                },
                payload=b"",
            )
            current_last_id = user.tg_id

        meta["last_handled_tg_id"] = current_last_id
        await self.kv.put(mailing_id, json.dumps(meta).encode())

        # Trigger next batch
        await self.js.publish(subject=self.subject, payload=mailing_id.encode())
        await msg.ack()

        logger.debug(
            f"Batch processed. Last ID: {meta.get("last_handled_tg_id")} "
            "Next batch triggered"
        )

    async def _finish_mailing(self, mailing_id: str, meta: dict) -> None:
        meta["status"] = "COMPLETED"
        await self.kv.put(mailing_id, json.dumps(meta).encode())
        logger.debug(f"Mailing {mailing_id} completed successfully.")

    async def stop(self) -> None:
        self._is_running = False
