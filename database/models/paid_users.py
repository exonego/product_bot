from __future__ import annotations
from datetime import datetime

from sqlalchemy import (
    BigInteger,
    Enum,
    Text,
    Boolean,
    DateTime,
    text,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column

from database import Base
from bot.enums import Role


class PaidUser(Base):
    __tablename__ = "paid_users"

    tg_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    role: Mapped[Role] = mapped_column(Enum(Role), nullable=False)
    language: Mapped[str] = mapped_column(Text, nullable=False)
    banned: Mapped[bool] = mapped_column(
        Boolean, nullable=False, server_default=text("false")
    )
    is_alive: Mapped[bool] = mapped_column(
        Boolean, nullable=False, server_default=text("false")
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
