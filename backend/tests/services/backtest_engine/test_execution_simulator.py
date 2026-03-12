from __future__ import annotations

from datetime import UTC, date, datetime

import pytest

from app.services.backtest_engine.execution import ExecutionService, MinuteBar


@pytest.fixture
def execution_service() -> ExecutionService:
    return ExecutionService()


@pytest.fixture
def minute_bars() -> list[MinuteBar]:
    return [
        MinuteBar(
            bar_time=datetime(2025, 1, 6, 9, 31, tzinfo=UTC),
            open=10.0,
            high=10.2,
            low=9.9,
            close=10.1,
            volume=100_000,
        ),
        MinuteBar(
            bar_time=datetime(2025, 1, 6, 9, 32, tzinfo=UTC),
            open=10.1,
            high=10.3,
            low=10.0,
            close=10.2,
            volume=95_000,
        ),
    ]


def test_execution_simulator_applies_slippage_and_price_limits(
    execution_service: ExecutionService,
    minute_bars: list[MinuteBar],
) -> None:
    trade = execution_service.execute_buy(
        symbol="000001.SZ",
        signal_time=date(2025, 1, 6),
        minute_bars=minute_bars,
        slippage_bps=15,
    )

    assert trade.status == "filled"
    assert trade.price > minute_bars[0].open
    assert trade.filled_at == minute_bars[0].bar_time


def test_execution_simulator_skips_limit_up_bars_for_buy_orders(
    execution_service: ExecutionService,
    minute_bars: list[MinuteBar],
) -> None:
    minute_bars[0] = MinuteBar(
        bar_time=minute_bars[0].bar_time,
        open=minute_bars[0].open,
        high=minute_bars[0].high,
        low=minute_bars[0].low,
        close=minute_bars[0].close,
        volume=minute_bars[0].volume,
        is_limit_up=True,
    )

    trade = execution_service.execute_buy(
        symbol="000001.SZ",
        signal_time=date(2025, 1, 6),
        minute_bars=minute_bars,
        slippage_bps=15,
    )

    assert trade.status == "filled"
    assert trade.filled_at == minute_bars[1].bar_time
