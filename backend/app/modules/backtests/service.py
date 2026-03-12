from __future__ import annotations

from dataclasses import dataclass

from app.modules.backtests.repository import BacktestsRepository
from app.services.backtest_engine.execution import ExecutionService
from app.services.backtest_engine.metrics import MetricsService, PerformanceMetrics
from app.services.backtest_engine.portfolio import PortfolioService
from app.services.backtest_engine.signals import SignalService
from app.services.backtest_engine.snapshots import BacktestSnapshot


@dataclass(frozen=True, slots=True)
class BacktestRunResult:
    job_id: str
    status: str
    metrics: PerformanceMetrics


class BacktestsService:
    def __init__(
        self,
        repository: BacktestsRepository,
        *,
        signal_service: SignalService | None = None,
        execution_service: ExecutionService | None = None,
        portfolio_service: PortfolioService | None = None,
        metrics_service: MetricsService | None = None,
    ) -> None:
        self._repository = repository
        self._signal_service = signal_service or SignalService()
        self._execution_service = execution_service or ExecutionService()
        self._portfolio_service = portfolio_service or PortfolioService()
        self._metrics_service = metrics_service or MetricsService()

    def create_snapshot(self, *, strategy_instance_id: str, data_version: str = "latest") -> BacktestSnapshot:
        strategy_instance = self._repository.get_strategy_instance(strategy_instance_id)
        if strategy_instance is None:
            raise ValueError(f"strategy instance not found: {strategy_instance_id}")

        stock_pool = self._repository.get_stock_pool(strategy_instance.stock_pool_id)
        if stock_pool is None:
            raise ValueError(f"stock pool not found: {strategy_instance.stock_pool_id}")

        return BacktestSnapshot.from_strategy(
            strategy_instance=strategy_instance,
            stock_pool=stock_pool,
            data_version=data_version,
        )

    def run_backtest(
        self,
        *,
        strategy_instance_id: str,
        current_user_id: str | None = None,
    ) -> BacktestRunResult:
        strategy_instance = self._repository.get_strategy_instance(strategy_instance_id)
        if strategy_instance is None:
            raise ValueError(f"strategy instance not found: {strategy_instance_id}")
        if current_user_id is not None and strategy_instance.created_by_user_id != current_user_id:
            raise ValueError(f"strategy instance not found: {strategy_instance_id}")

        snapshot = self.create_snapshot(strategy_instance_id=strategy_instance_id)
        job = self._repository.create_job(strategy_instance_id=snapshot.strategy_instance_id)
        rebalance_date, daily_inputs = self._repository.get_latest_daily_inputs(list(snapshot.stock_pool_symbols))
        signal = self._signal_service.generate(
            rebalance_date=rebalance_date,
            snapshot=snapshot,
            daily_inputs=daily_inputs,
        )

        fills = [
            self._execution_service.execute_buy(
                symbol=symbol,
                signal_time=rebalance_date,
                minute_bars=self._repository.get_latest_minute_bars(symbol),
                slippage_bps=snapshot.slippage_bps,
                commission_bps=snapshot.commission_bps,
            )
            for symbol in signal.target_symbols
        ]
        portfolio = self._portfolio_service.build(
            fills=fills,
            exit_prices=self._repository.get_latest_daily_closes(signal.target_symbols),
        )
        metrics = self._metrics_service.calculate(equity_curve=portfolio.equity_curve)
        completed_job, _ = self._repository.complete_job(
            job_id=job.id,
            total_return=metrics.total_return,
            max_drawdown=metrics.max_drawdown,
        )
        return BacktestRunResult(
            job_id=completed_job.id,
            status=completed_job.status,
            metrics=metrics,
        )
