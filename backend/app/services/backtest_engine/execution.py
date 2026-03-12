from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime

from app.services.backtest_engine.fees import apply_slippage, calculate_commission
from app.services.backtest_engine.limits import is_tradeable


@dataclass(frozen=True, slots=True)
class MinuteBar:
    bar_time: datetime
    open: float
    high: float
    low: float
    close: float
    volume: float
    is_limit_up: bool = False
    is_limit_down: bool = False


@dataclass(frozen=True, slots=True)
class TradeFill:
    symbol: str
    status: str
    price: float | None
    filled_at: datetime | None
    commission: float


class ExecutionService:
    def execute_buy(
        self,
        *,
        symbol: str,
        signal_time: date,
        minute_bars: list[MinuteBar],
        slippage_bps: float,
        commission_bps: float = 0,
    ) -> TradeFill:
        del signal_time

        candidate_bar = next((bar for bar in minute_bars if is_tradeable(bar, order_side="buy")), None)
        if candidate_bar is None:
            return TradeFill(symbol=symbol, status="rejected", price=None, filled_at=None, commission=0.0)

        price = apply_slippage(candidate_bar.open, slippage_bps, order_side="buy")
        commission = calculate_commission(price, commission_bps)
        return TradeFill(
            symbol=symbol,
            status="filled",
            price=price,
            filled_at=candidate_bar.bar_time,
            commission=commission,
        )
