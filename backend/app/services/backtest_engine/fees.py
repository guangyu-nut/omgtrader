from __future__ import annotations


def apply_slippage(price: float, slippage_bps: float, *, order_side: str) -> float:
    direction = 1 if order_side == "buy" else -1
    return price * (1 + direction * slippage_bps / 10_000)


def calculate_commission(notional: float, commission_bps: float) -> float:
    return notional * commission_bps / 10_000
