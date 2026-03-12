from __future__ import annotations

from fastapi import HTTPException

from app.modules.results.repository import ResultsRepository
from app.modules.results.schemas import BacktestResultDetail, CurvePointDto, MetricsDto


class ResultsService:
    def __init__(self, repository: ResultsRepository) -> None:
        self._repository = repository

    def get_backtest_result(self, *, job_id: str, current_user_id: str) -> BacktestResultDetail:
        job, metric, strategy = self._repository.get_backtest_result_record(job_id=job_id)
        if job is None or strategy is None or strategy.created_by_user_id != current_user_id:
            raise HTTPException(status_code=404, detail="backtest result not found")

        total_return = metric.total_return if metric is not None and metric.total_return is not None else 0.0
        max_drawdown = metric.max_drawdown if metric is not None else None

        return BacktestResultDetail(
            metrics=MetricsDto(
                total_return=metric.total_return if metric is not None else None,
                max_drawdown=max_drawdown,
            ),
            equity_curve=[
                CurvePointDto(label="起点", value=1.0),
                CurvePointDto(label="终点", value=1.0 + total_return),
            ],
            rebalances=[],
        )
