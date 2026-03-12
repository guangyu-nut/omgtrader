from __future__ import annotations

from datetime import datetime
from uuid import uuid4

from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


def _uuid() -> str:
    return str(uuid4())


class BacktestJob(Base):
    __tablename__ = "backtest_jobs"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_uuid)
    strategy_instance_id: Mapped[str] = mapped_column(ForeignKey("strategy_instances.id"), nullable=False)
    status: Mapped[str] = mapped_column(String(32), nullable=False)
    started_at: Mapped[datetime | None] = mapped_column(DateTime(), nullable=True)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(), nullable=True)
