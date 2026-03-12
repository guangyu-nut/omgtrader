from __future__ import annotations

from datetime import UTC, datetime
from uuid import uuid4

from sqlalchemy import JSON, DateTime, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


def _uuid() -> str:
    return str(uuid4())


class AiInsight(Base):
    __tablename__ = "ai_insights"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_uuid)
    backtest_job_id: Mapped[str] = mapped_column(ForeignKey("backtest_jobs.id"), unique=True, nullable=False)
    summary: Mapped[str] = mapped_column(Text(), nullable=False)
    risks: Mapped[list[str]] = mapped_column(JSON(), nullable=False, default=list)
    created_at: Mapped[datetime] = mapped_column(DateTime(), default=lambda: datetime.now(UTC), nullable=False)
