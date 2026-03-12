from __future__ import annotations

from app.modules.backtests.repository import BacktestsRepository
from app.services.backtest_engine.snapshots import BacktestSnapshot


class BacktestsService:
    def __init__(self, repository: BacktestsRepository) -> None:
        self._repository = repository

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
