from __future__ import annotations

from datetime import date

import pytest

from app.services.backtest_engine.signals import DailySignalInput, SignalService
from app.services.backtest_engine.snapshots import BacktestSnapshot


@pytest.fixture
def signal_service() -> SignalService:
    return SignalService()


@pytest.fixture
def top_n_snapshot() -> BacktestSnapshot:
    return BacktestSnapshot(
        strategy_instance_id="strategy-1",
        strategy_name="Top N demo",
        template_type="top_n_equal_weight",
        stock_pool_id="pool-1",
        stock_pool_name="CSI300 manual",
        stock_pool_symbols=("000001.SZ", "600000.SH", "000002.SZ"),
        ranking_metric="close",
        hold_count=2,
        rebalance_frequency="daily",
        slippage_bps=15,
        commission_bps=5,
        benchmark_symbol="000300.SH",
        data_version="latest",
    )


@pytest.fixture
def ranked_daily_inputs() -> list[DailySignalInput]:
    return [
        DailySignalInput(symbol="000001.SZ", values={"close": 11.2}),
        DailySignalInput(symbol="600000.SH", values={"close": 12.7}),
        DailySignalInput(symbol="000002.SZ", values={"close": 10.5}),
    ]


def test_top_n_equal_weight_signal_selects_highest_ranked_symbols(
    signal_service: SignalService,
    top_n_snapshot: BacktestSnapshot,
    ranked_daily_inputs: list[DailySignalInput],
) -> None:
    signal = signal_service.generate(
        rebalance_date=date(2025, 1, 3),
        snapshot=top_n_snapshot,
        daily_inputs=ranked_daily_inputs,
    )

    assert signal.target_symbols == ["600000.SH", "000001.SZ"]
