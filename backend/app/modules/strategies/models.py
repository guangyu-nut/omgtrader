from __future__ import annotations

from datetime import datetime, UTC
from uuid import uuid4

from sqlalchemy import DateTime, Float, ForeignKey, Integer, JSON, String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


def _uuid() -> str:
    return str(uuid4())


class StrategyInstance(Base):
    __tablename__ = "strategy_instances"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_uuid)
    name: Mapped[str] = mapped_column(String(128), nullable=False)
    template_type: Mapped[str] = mapped_column(String(64), nullable=False)
    stock_pool_id: Mapped[str] = mapped_column(ForeignKey("stock_pools.id"), nullable=False)
    ranking_metric: Mapped[str] = mapped_column(String(64), nullable=False)
    hold_count: Mapped[int] = mapped_column(Integer(), nullable=False)
    rebalance_frequency: Mapped[str] = mapped_column(String(32), nullable=False, default="daily")
    slippage_bps: Mapped[float] = mapped_column(Float(), nullable=False, default=0.0)
    commission_bps: Mapped[float] = mapped_column(Float(), nullable=False, default=0.0)
    benchmark_symbol: Mapped[str] = mapped_column(String(32), nullable=False, default="000300.SH")
    created_by_user_id: Mapped[str] = mapped_column(ForeignKey("users.id"), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(), default=lambda: datetime.now(UTC), nullable=False)


class StockPool(Base):
    __tablename__ = "stock_pools"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_uuid)
    name: Mapped[str] = mapped_column(String(128), nullable=False)
    input_mode: Mapped[str] = mapped_column(String(32), nullable=False)
    symbols: Mapped[list[str]] = mapped_column(JSON(), nullable=False, default=list)
    created_by_user_id: Mapped[str] = mapped_column(ForeignKey("users.id"), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(), default=lambda: datetime.now(UTC), nullable=False)
