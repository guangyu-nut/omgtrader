from __future__ import annotations

from sqlalchemy.orm import Session

from app.modules.strategies.models import StockPool, StrategyInstance


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
