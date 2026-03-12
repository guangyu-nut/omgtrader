from __future__ import annotations

from app.modules.auth.models import User
from app.modules.strategies.repository import StrategiesRepository
from app.modules.strategies.schemas import StockPoolCreate, StrategyInstanceCreate


class StrategiesService:
    def __init__(self, repository: StrategiesRepository) -> None:
        self._repository = repository

    def create_stock_pool(self, payload: StockPoolCreate, current_user: User):
        return self._repository.create_stock_pool(
            name=payload.name,
            input_mode=payload.input_mode,
            symbols=payload.symbols,
            created_by_user_id=current_user.id,
        )

    def create_strategy_instance(self, payload: StrategyInstanceCreate, current_user: User):
        return self._repository.create_strategy_instance(
            name=payload.name,
            template_type=payload.template_type,
            stock_pool_id=payload.stock_pool_id,
            ranking_metric=payload.ranking_metric,
            hold_count=payload.hold_count,
            rebalance_frequency=payload.rebalance_frequency,
            slippage_bps=payload.slippage_bps,
            commission_bps=payload.commission_bps,
            benchmark_symbol=payload.benchmark_symbol,
            created_by_user_id=current_user.id,
        )
