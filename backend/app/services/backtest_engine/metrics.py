from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class PerformanceMetrics:
    total_return: float
    max_drawdown: float


class MetricsService:
    def calculate(self, *, equity_curve: list[float]) -> PerformanceMetrics:
        if not equity_curve:
            return PerformanceMetrics(total_return=0.0, max_drawdown=0.0)

        starting_value = equity_curve[0]
        total_return = (equity_curve[-1] / starting_value - 1) if starting_value else 0.0

        peak = equity_curve[0]
        max_drawdown = 0.0
        for value in equity_curve:
            peak = max(peak, value)
            if peak:
                max_drawdown = max(max_drawdown, (peak - value) / peak)

        return PerformanceMetrics(total_return=total_return, max_drawdown=max_drawdown)
