from __future__ import annotations

from datetime import UTC, datetime

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.modules.strategies.models import PythonStrategy, StockPool, StrategyInstance


class StrategiesRepository:
    def __init__(self, db_session: Session) -> None:
        self._db_session = db_session

    def create_stock_pool(self, *, name: str, input_mode: str, symbols: list[str], created_by_user_id: str) -> StockPool:
        stock_pool = StockPool(
            name=name,
            input_mode=input_mode,
            symbols=symbols,
            created_by_user_id=created_by_user_id,
        )
        self._db_session.add(stock_pool)
        self._db_session.commit()
        self._db_session.refresh(stock_pool)
        return stock_pool

    def create_strategy_instance(
        self,
        *,
        name: str,
        template_type: str,
        stock_pool_id: str,
        ranking_metric: str,
        hold_count: int,
        rebalance_frequency: str,
        slippage_bps: float,
        commission_bps: float,
        benchmark_symbol: str,
        created_by_user_id: str,
    ) -> StrategyInstance:
        strategy = StrategyInstance(
            name=name,
            template_type=template_type,
            stock_pool_id=stock_pool_id,
            ranking_metric=ranking_metric,
            hold_count=hold_count,
            rebalance_frequency=rebalance_frequency,
            slippage_bps=slippage_bps,
            commission_bps=commission_bps,
            benchmark_symbol=benchmark_symbol,
            created_by_user_id=created_by_user_id,
        )
        self._db_session.add(strategy)
        self._db_session.commit()
        self._db_session.refresh(strategy)
        return strategy

    def create_python_strategy(
        self,
        *,
        user_id: str,
        name: str,
        description: str,
        tags_text: str,
        parameter_schema_text: str,
        code: str,
    ) -> PythonStrategy:
        strategy = PythonStrategy(
            user_id=user_id,
            name=name,
            description=description,
            tags_text=tags_text,
            parameter_schema_text=parameter_schema_text,
            code=code,
        )
        self._db_session.add(strategy)
        self._db_session.commit()
        self._db_session.refresh(strategy)
        return strategy

    def list_python_strategies(self, *, user_id: str) -> list[PythonStrategy]:
        statement = (
            select(PythonStrategy)
            .where(PythonStrategy.user_id == user_id)
            .order_by(PythonStrategy.updated_at.desc(), PythonStrategy.created_at.desc())
        )
        return list(self._db_session.scalars(statement))

    def get_python_strategy(self, *, strategy_id: str, user_id: str) -> PythonStrategy | None:
        statement = select(PythonStrategy).where(PythonStrategy.id == strategy_id, PythonStrategy.user_id == user_id)
        return self._db_session.scalar(statement)

    def update_python_strategy(
        self,
        strategy: PythonStrategy,
        *,
        name: str,
        description: str,
        tags_text: str,
        parameter_schema_text: str,
        code: str,
    ) -> PythonStrategy:
        strategy.name = name
        strategy.description = description
        strategy.tags_text = tags_text
        strategy.parameter_schema_text = parameter_schema_text
        strategy.code = code
        strategy.updated_at = datetime.now(UTC)

        self._db_session.commit()
        self._db_session.refresh(strategy)
        return strategy

    def delete_python_strategy(self, strategy: PythonStrategy) -> None:
        self._db_session.delete(strategy)
        self._db_session.commit()
