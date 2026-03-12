from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.modules.ai_assistant.models import AiInsight
from app.modules.backtests.models import BacktestJob
from app.modules.results.models import BacktestMetric
from app.modules.strategies.models import StrategyInstance


class AiAssistantRepository:
    def __init__(self, db_session: Session) -> None:
        self._db_session = db_session

    def get_backtest_context(
        self,
        *,
        job_id: str,
    ) -> tuple[BacktestJob | None, BacktestMetric | None, StrategyInstance | None]:
        job = self._db_session.get(BacktestJob, job_id)
        if job is None:
            return None, None, None

        metric = (
            self._db_session.execute(
                select(BacktestMetric).where(BacktestMetric.backtest_job_id == job_id)
            ).scalar_one_or_none()
        )
        strategy = self._db_session.get(StrategyInstance, job.strategy_instance_id)
        return job, metric, strategy

    def save_insight(self, *, job_id: str, summary: str, risks: list[str]) -> AiInsight:
        insight = (
            self._db_session.execute(
                select(AiInsight).where(AiInsight.backtest_job_id == job_id)
            ).scalar_one_or_none()
        )
        if insight is None:
            insight = AiInsight(backtest_job_id=job_id, summary=summary, risks=risks)
            self._db_session.add(insight)
        else:
            insight.summary = summary
            insight.risks = risks

        self._db_session.commit()
        self._db_session.refresh(insight)
        return insight
