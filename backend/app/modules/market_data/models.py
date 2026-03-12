from __future__ import annotations

from datetime import UTC, date, datetime
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


class DataSourceConfig(Base):
    __tablename__ = "data_source_configs"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_uuid)
    name: Mapped[str] = mapped_column(String(64), nullable=False)
    provider_type: Mapped[str] = mapped_column(String(32), nullable=False)
    enabled: Mapped[bool] = mapped_column(Boolean(), default=True, nullable=False)
    created_by_user_id: Mapped[str] = mapped_column(ForeignKey("users.id"), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(), default=lambda: datetime.now(UTC), nullable=False)


class DataSyncTask(Base):
    __tablename__ = "data_sync_tasks"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_uuid)
    data_source_config_id: Mapped[str] = mapped_column(ForeignKey("data_source_configs.id"), nullable=False)
    status: Mapped[str] = mapped_column(String(32), nullable=False, default="pending")
    started_at: Mapped[datetime | None] = mapped_column(DateTime(), nullable=True)
    finished_at: Mapped[datetime | None] = mapped_column(DateTime(), nullable=True)
