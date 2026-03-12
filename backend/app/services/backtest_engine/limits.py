from __future__ import annotations

from typing import Protocol


class LimitAwareBar(Protocol):
    is_limit_up: bool
    is_limit_down: bool


def is_tradeable(bar: LimitAwareBar, *, order_side: str) -> bool:
    if order_side == "buy":
        return not bar.is_limit_up

    return not bar.is_limit_down
