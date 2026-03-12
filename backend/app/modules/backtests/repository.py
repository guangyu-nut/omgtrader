from __future__ import annotations

from datetime import UTC, date, datetime

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.modules.backtests.models import BacktestJob
from app.modules.market_data.models import BarDaily, BarMinute, Symbol
from app.modules.results.models import BacktestMetric
from app.modules.strategies.models import StockPool, StrategyInstance
from app.services.backtest_engine.execution import MinuteBar
from app.services.backtest_engine.signals import DailySignalInput


class BacktestsRepository:
    def __init__(self, db_session: Session) -> None:
        self._db_session = db_session

    def get_strategy_instance(self, strategy_instance_id: str) -> StrategyInstance | None:
        return self._db_session.get(StrategyInstance, strategy_instance_id)

    def get_stock_pool(self, stock_pool_id: str) -> StockPool | None:
        return self._db_session.get(StockPool, stock_pool_id)

    def get_latest_daily_inputs(self, symbol_codes: list[str]) -> tuple[date, list[DailySignalInput]]:
        rows = self._db_session.execute(
            select(
                Symbol.code,
                BarDaily.trade_date,
                BarDaily.open,
                BarDaily.high,
                BarDaily.low,
                BarDaily.close,
                BarDaily.volume,
            )
            .join(BarDaily, Symbol.id == BarDaily.symbol_id)
            .where(Symbol.code.in_(symbol_codes))
        ).all()
        if not rows:
            raise ValueError("no daily bars available for stock pool")

        latest_trade_date = max(row.trade_date for row in rows)
        return latest_trade_date, [
            DailySignalInput(
                symbol=row.code,
                values={
                    "open": row.open,
                    "high": row.high,
                    "low": row.low,
                    "close": row.close,
                    "volume": row.volume,
                },
            )
            for row in rows
            if row.trade_date == latest_trade_date
        ]

    def get_latest_daily_closes(self, symbol_codes: list[str]) -> dict[str, float]:
        rows = self._db_session.execute(
            select(Symbol.code, BarDaily.trade_date, BarDaily.close)
            .join(BarDaily, Symbol.id == BarDaily.symbol_id)
            .where(Symbol.code.in_(symbol_codes))
        ).all()
        if not rows:
            return {}

        latest_by_symbol: dict[str, tuple[date, float]] = {}
        for row in rows:
            current = latest_by_symbol.get(row.code)
            if current is None or row.trade_date > current[0]:
                latest_by_symbol[row.code] = (row.trade_date, row.close)

        return {code: item[1] for code, item in latest_by_symbol.items()}

    def get_latest_minute_bars(self, symbol_code: str) -> list[MinuteBar]:
        rows = self._db_session.execute(
            select(
                BarMinute.bar_time,
                BarMinute.open,
                BarMinute.high,
                BarMinute.low,
                BarMinute.close,
                BarMinute.volume,
            )
            .join(Symbol, Symbol.id == BarMinute.symbol_id)
            .where(Symbol.code == symbol_code)
            .order_by(BarMinute.bar_time.asc())
        ).all()
        if not rows:
            raise ValueError(f"no minute bars available for {symbol_code}")

        latest_bar_date = max(row.bar_time.date() for row in rows)
        return [
            MinuteBar(
                bar_time=row.bar_time,
                open=row.open,
                high=row.high,
                low=row.low,
                close=row.close,
                volume=row.volume,
            )
            for row in rows
            if row.bar_time.date() == latest_bar_date
        ]

    def create_job(self, *, strategy_instance_id: str, status: str = "running") -> BacktestJob:
        job = BacktestJob(
            strategy_instance_id=strategy_instance_id,
            status=status,
            started_at=datetime.now(UTC),
        )
        self._db_session.add(job)
        self._db_session.commit()
        self._db_session.refresh(job)
        return job

    def complete_job(
        self,
        *,
        job_id: str,
        total_return: float,
        max_drawdown: float,
    ) -> tuple[BacktestJob, BacktestMetric]:
        job = self._db_session.get(BacktestJob, job_id)
        if job is None:
            raise ValueError(f"backtest job not found: {job_id}")

        metric = (
            self._db_session.execute(
                select(BacktestMetric).where(BacktestMetric.backtest_job_id == job_id)
            ).scalar_one_or_none()
        )
        if metric is None:
            metric = BacktestMetric(backtest_job_id=job_id)
            self._db_session.add(metric)

        job.status = "completed"
        job.completed_at = datetime.now(UTC)
        metric.total_return = total_return
        metric.max_drawdown = max_drawdown

        self._db_session.commit()
        self._db_session.refresh(job)
        self._db_session.refresh(metric)
        return job, metric
