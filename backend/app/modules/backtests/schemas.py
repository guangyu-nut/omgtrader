from __future__ import annotations

from pydantic import BaseModel


class BacktestJobCreate(BaseModel):
    strategy_instance_id: str


class BacktestMetricsRead(BaseModel):
    total_return: float | None
    max_drawdown: float | None


class BacktestJobRead(BaseModel):
    id: str
    status: str
    metrics: BacktestMetricsRead


class BacktestSnapshotRead(BaseModel):
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
