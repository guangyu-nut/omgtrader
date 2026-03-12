from __future__ import annotations

from dataclasses import dataclass

from app.modules.strategies.models import StockPool, StrategyInstance


@dataclass(frozen=True, slots=True)
class BacktestSnapshot:
    strategy_instance_id: str
    strategy_name: str
    template_type: str
    stock_pool_id: str
    stock_pool_name: str
    stock_pool_symbols: tuple[str, ...]
    ranking_metric: str
    hold_count: int
    rebalance_frequency: str
    slippage_bps: float
    commission_bps: float
    benchmark_symbol: str
    data_version: str

    @classmethod
    def from_strategy(
        cls,
        *,
        strategy_instance: StrategyInstance,
        stock_pool: StockPool,
        data_version: str,
    ) -> "BacktestSnapshot":
        return cls(
            strategy_instance_id=strategy_instance.id,
            strategy_name=strategy_instance.name,
            template_type=strategy_instance.template_type,
            stock_pool_id=stock_pool.id,
            stock_pool_name=stock_pool.name,
            stock_pool_symbols=tuple(stock_pool.symbols),
            ranking_metric=strategy_instance.ranking_metric,
            hold_count=strategy_instance.hold_count,
            rebalance_frequency=strategy_instance.rebalance_frequency,
            slippage_bps=strategy_instance.slippage_bps,
            commission_bps=strategy_instance.commission_bps,
            benchmark_symbol=strategy_instance.benchmark_symbol,
            data_version=data_version,
        )
