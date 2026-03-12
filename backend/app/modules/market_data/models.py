from __future__ import annotations

from datetime import date, datetime
from uuid import uuid4

from sqlalchemy import Boolean, Date, DateTime, Float, ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


def _uuid() -> str:
    return str(uuid4())


class Symbol(Base):
    __tablename__ = "symbols"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_uuid)
    code: Mapped[str] = mapped_column(String(16), unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(128), nullable=False)
    market: Mapped[str] = mapped_column(String(16), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), default=True, nullable=False)


class BarDaily(Base):
    __tablename__ = "bar_daily"
    __table_args__ = (UniqueConstraint("symbol_id", "trade_date"),)

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_uuid)
    symbol_id: Mapped[str] = mapped_column(ForeignKey("symbols.id"), nullable=False)
    trade_date: Mapped[date] = mapped_column(Date(), nullable=False)
    open: Mapped[float] = mapped_column(Float(), nullable=False)
    high: Mapped[float] = mapped_column(Float(), nullable=False)
    low: Mapped[float] = mapped_column(Float(), nullable=False)
    close: Mapped[float] = mapped_column(Float(), nullable=False)
    volume: Mapped[float] = mapped_column(Float(), nullable=False)


class BarMinute(Base):
    __tablename__ = "bar_minute"
    __table_args__ = (UniqueConstraint("symbol_id", "bar_time"),)

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_uuid)
    symbol_id: Mapped[str] = mapped_column(ForeignKey("symbols.id"), nullable=False)
    bar_time: Mapped[datetime] = mapped_column(DateTime(), nullable=False)
    open: Mapped[float] = mapped_column(Float(), nullable=False)
    high: Mapped[float] = mapped_column(Float(), nullable=False)
    low: Mapped[float] = mapped_column(Float(), nullable=False)
    close: Mapped[float] = mapped_column(Float(), nullable=False)
    volume: Mapped[float] = mapped_column(Float(), nullable=False)
