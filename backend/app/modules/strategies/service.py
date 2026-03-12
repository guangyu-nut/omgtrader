from __future__ import annotations

from fastapi import HTTPException

from app.modules.auth.models import User
from app.modules.strategies.models import PythonStrategy
from app.modules.strategies.repository import StrategiesRepository
from app.modules.strategies.schemas import (
    PythonStrategyCreate,
    PythonStrategyListItem,
    PythonStrategyRead,
    PythonStrategyUpdate,
    StockPoolCreate,
    StrategyInstanceCreate,
)


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

    def list_python_strategies(self, current_user: User) -> list[PythonStrategyListItem]:
        return [self._to_list_item(strategy) for strategy in self._repository.list_python_strategies(user_id=current_user.id)]

    def get_python_strategy(self, strategy_id: str, current_user: User) -> PythonStrategyRead:
        strategy = self._repository.get_python_strategy(strategy_id=strategy_id, user_id=current_user.id)
        if strategy is None:
            raise HTTPException(status_code=404, detail="python strategy not found")

        return self._to_read_model(strategy)

    def create_python_strategy(self, payload: PythonStrategyCreate, current_user: User) -> PythonStrategyRead:
        strategy = self._repository.create_python_strategy(
            user_id=current_user.id,
            name=payload.name,
            description=payload.description,
            tags_text=self._serialize_tags(payload.tags),
            parameter_schema_text=payload.parameter_schema_text,
            code=payload.code,
        )
        return self._to_read_model(strategy)

    def update_python_strategy(
        self,
        strategy_id: str,
        payload: PythonStrategyUpdate,
        current_user: User,
    ) -> PythonStrategyRead:
        strategy = self._repository.get_python_strategy(strategy_id=strategy_id, user_id=current_user.id)
        if strategy is None:
            raise HTTPException(status_code=404, detail="python strategy not found")

        updated = self._repository.update_python_strategy(
            strategy,
            name=payload.name,
            description=payload.description,
            tags_text=self._serialize_tags(payload.tags),
            parameter_schema_text=payload.parameter_schema_text,
            code=payload.code,
        )
        return self._to_read_model(updated)

    def delete_python_strategy(self, strategy_id: str, current_user: User) -> None:
        strategy = self._repository.get_python_strategy(strategy_id=strategy_id, user_id=current_user.id)
        if strategy is None:
            raise HTTPException(status_code=404, detail="python strategy not found")

        self._repository.delete_python_strategy(strategy)

    @staticmethod
    def _serialize_tags(tags: list[str]) -> str:
        return ",".join(tag for tag in (item.strip() for item in tags) if tag)

    @staticmethod
    def _deserialize_tags(tags_text: str) -> list[str]:
        return [tag for tag in (item.strip() for item in tags_text.split(",")) if tag]

    def _to_list_item(self, strategy: PythonStrategy) -> PythonStrategyListItem:
        return PythonStrategyListItem(
            id=strategy.id,
            name=strategy.name,
            description=strategy.description,
            tags=self._deserialize_tags(strategy.tags_text),
            updated_at=strategy.updated_at,
        )

    def _to_read_model(self, strategy: PythonStrategy) -> PythonStrategyRead:
        return PythonStrategyRead(
            id=strategy.id,
            name=strategy.name,
            description=strategy.description,
            tags=self._deserialize_tags(strategy.tags_text),
            parameter_schema_text=strategy.parameter_schema_text,
            code=strategy.code,
            created_at=strategy.created_at,
            updated_at=strategy.updated_at,
        )
