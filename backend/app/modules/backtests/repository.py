from __future__ import annotations

from sqlalchemy.orm import Session

from app.modules.strategies.models import StockPool, StrategyInstance


class BacktestsRepository:
    def __init__(self, db_session: Session) -> None:
        self._db_session = db_session

    def get_strategy_instance(self, strategy_instance_id: str) -> StrategyInstance | None:
        return self._db_session.get(StrategyInstance, strategy_instance_id)

    def get_stock_pool(self, stock_pool_id: str) -> StockPool | None:
        return self._db_session.get(StockPool, stock_pool_id)
