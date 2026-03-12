from __future__ import annotations

from pydantic import BaseModel


class MetricsDto(BaseModel):
    total_return: float | None
    max_drawdown: float | None


class CurvePointDto(BaseModel):
    label: str
    value: float


class RebalanceDto(BaseModel):
    symbol: str
    action: str


class BacktestResultDetail(BaseModel):
    metrics: MetricsDto
    equity_curve: list[CurvePointDto]
    rebalances: list[RebalanceDto]
