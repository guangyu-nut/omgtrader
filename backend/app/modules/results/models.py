from __future__ import annotations

from uuid import uuid4

from sqlalchemy import Float, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


def _uuid() -> str:
    return str(uuid4())


class BacktestMetric(Base):
    __tablename__ = "backtest_metrics"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_uuid)
    backtest_job_id: Mapped[str] = mapped_column(ForeignKey("backtest_jobs.id"), unique=True, nullable=False)
    total_return: Mapped[float | None] = mapped_column(Float(), nullable=True)
    max_drawdown: Mapped[float | None] = mapped_column(Float(), nullable=True)
