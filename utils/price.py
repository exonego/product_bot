import logging
from decimal import Decimal, InvalidOperation

from redis.asyncio import Redis

logger = logging.getLogger(__name__)


async def get_price(redis: Redis) -> Decimal | None:
    """Gets current product price from Redis"""

    product_price = await redis.get("product_price")

    if product_price is None:
        return None

    try:
        return Decimal(product_price.decode("utf-8"))
    except (InvalidOperation, ValueError):
        return None


async def set_price(redis: Redis, price: Decimal) -> None:
    """Sets new product price"""

    await redis.set("product_price", str(price))
