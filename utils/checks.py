import re
from datetime import datetime


def price_check(text: str) -> str:
    price_parts = text.strip().split(".")
    if (
        len(price_parts) == 2
        and price_parts[0].isdigit()
        and len(price_parts[1]) == 2
        and price_parts[1].isdigit()
    ):
        return text.strip()
    raise ValueError


def user_id_check(text: str) -> str:
    only_digits = re.sub(r"\D", "", text)
    if only_digits:
        return only_digits
    raise ValueError


def date_check(text: str) -> str:
    datetime.strptime(text.strip(), "%d.%m.%Y")
    return text.strip()
