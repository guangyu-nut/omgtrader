from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field


class StockPoolCreate(BaseModel):
    name: str
    input_mode: Literal["manual", "csv", "index_members"]
    symbols: list[str] = Field(default_factory=list)


class StockPoolRead(BaseModel):
    id: str
    name: str
    input_mode: str
    symbols: list[str]

    model_config = {"from_attributes": True}


class StrategyInstanceCreate(BaseModel):
    name: str
    template_type: Literal["top_n_equal_weight"]
    stock_pool_id: str
    ranking_metric: str
    hold_count: int
    rebalance_frequency: Literal["daily"]
    slippage_bps: float = 0
    commission_bps: float = 0
    benchmark_symbol: str = "000300.SH"


class StrategyInstanceRead(BaseModel):
    id: str
    name: str
    template_type: str
    stock_pool_id: str
    ranking_metric: str
    hold_count: int
    rebalance_frequency: str
    slippage_bps: float
    commission_bps: float
    benchmark_symbol: str

    model_config = {"from_attributes": True}
