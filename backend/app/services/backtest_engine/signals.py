from __future__ import annotations

from dataclasses import dataclass
from datetime import date

from app.services.backtest_engine.snapshots import BacktestSnapshot


@dataclass(frozen=True, slots=True)
class DailySignalInput:
    symbol: str
    values: dict[str, float]


@dataclass(frozen=True, slots=True)
class RebalanceSignal:
    rebalance_date: date
    target_symbols: list[str]


class SignalService:
    def generate(
        self,
        *,
        rebalance_date: date,
        snapshot: BacktestSnapshot,
        daily_inputs: list[DailySignalInput],
    ) -> RebalanceSignal:
        if snapshot.template_type != "top_n_equal_weight":
            raise ValueError(f"unsupported template type: {snapshot.template_type}")

        eligible_inputs = [
            candidate
            for candidate in daily_inputs
            if candidate.symbol in snapshot.stock_pool_symbols and snapshot.ranking_metric in candidate.values
        ]
        ranked_inputs = sorted(
            eligible_inputs,
            key=lambda candidate: candidate.values[snapshot.ranking_metric],
            reverse=True,
        )

        return RebalanceSignal(
            rebalance_date=rebalance_date,
            target_symbols=[candidate.symbol for candidate in ranked_inputs[: snapshot.hold_count]],
        )
