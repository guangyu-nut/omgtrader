from __future__ import annotations

from datetime import datetime, UTC
from uuid import uuid4

from sqlalchemy import DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


def _uuid() -> str:
    return str(uuid4())


class StrategyInstance(Base):
    __tablename__ = "strategy_instances"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_uuid)
    name: Mapped[str] = mapped_column(String(128), nullable=False)
    template_type: Mapped[str] = mapped_column(String(64), nullable=False)
    ranking_metric: Mapped[str] = mapped_column(String(64), nullable=False)
    hold_count: Mapped[int] = mapped_column(Integer(), nullable=False)
    rebalance_frequency: Mapped[str] = mapped_column(String(32), nullable=False, default="daily")
    created_by_user_id: Mapped[str] = mapped_column(ForeignKey("users.id"), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(), default=lambda: datetime.now(UTC), nullable=False)
