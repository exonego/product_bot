from __future__ import annotations
from typing import TYPE_CHECKING
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
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base
from bot.enums import Role

if TYPE_CHECKING:
    from .actions import Action


class User(Base):
    __tablename__ = "users"

    tg_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    role: Mapped[Role] = mapped_column(Enum(Role), nullable=False)
    language: Mapped[str] = mapped_column(Text, nullable=False)
    banned: Mapped[bool] = mapped_column(
        Boolean, nullable=False, server_default=text("false")
    )
    is_alive: Mapped[bool] = mapped_column(
        Boolean, nullable=False, server_default=text("true")
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )

    actions: Mapped[list[Action]] = relationship(
        back_populates="user", cascade="delete", lazy="selectin"
    )
