from __future__ import annotations

from datetime import UTC, date, datetime

import pytest


def _seed_backtest_inputs(session, *, user_id: str) -> str:
    from app.modules.market_data.models import BarDaily, BarMinute, Symbol
    from app.modules.strategies.models import StockPool, StrategyInstance

    symbols = [
        Symbol(code="000001.SZ", name="Ping An Bank", market="SZ"),
        Symbol(code="600000.SH", name="Shanghai Bank", market="SH"),
        Symbol(code="000002.SZ", name="Vanke", market="SZ"),
    ]
    session.add_all(symbols)
    session.commit()

    symbol_by_code = {symbol.code: symbol for symbol in symbols}
    session.add_all(
        [
            BarDaily(
                symbol_id=symbol_by_code["000001.SZ"].id,
                trade_date=date(2025, 1, 3),
                open=10.0,
                high=10.4,
                low=9.9,
                close=10.2,
                volume=120_000,
            ),
            BarDaily(
                symbol_id=symbol_by_code["600000.SH"].id,
                trade_date=date(2025, 1, 3),
                open=12.0,
                high=12.5,
                low=11.9,
                close=12.3,
                volume=110_000,
            ),
            BarDaily(
                symbol_id=symbol_by_code["000002.SZ"].id,
                trade_date=date(2025, 1, 3),
                open=9.5,
                high=9.7,
                low=9.4,
                close=9.6,
                volume=90_000,
            ),
            BarMinute(
                symbol_id=symbol_by_code["000001.SZ"].id,
                bar_time=datetime(2025, 1, 6, 9, 31, tzinfo=UTC),
                open=10.05,
                high=10.2,
                low=10.0,
                close=10.2,
                volume=15_000,
            ),
            BarMinute(
                symbol_id=symbol_by_code["600000.SH"].id,
                bar_time=datetime(2025, 1, 6, 9, 31, tzinfo=UTC),
                open=12.05,
                high=12.3,
                low=12.0,
                close=12.3,
                volume=16_000,
            ),
            BarMinute(
                symbol_id=symbol_by_code["000002.SZ"].id,
                bar_time=datetime(2025, 1, 6, 9, 31, tzinfo=UTC),
                open=9.55,
                high=9.7,
                low=9.5,
                close=9.6,
                volume=14_000,
            ),
        ]
    )
    session.commit()

    stock_pool = StockPool(
        name="CSI300 manual",
        input_mode="manual",
        symbols=["000001.SZ", "600000.SH", "000002.SZ"],
        created_by_user_id=user_id,
    )
    session.add(stock_pool)
    session.commit()
    session.refresh(stock_pool)

    strategy = StrategyInstance(
        name="Top N demo",
        template_type="top_n_equal_weight",
        stock_pool_id=stock_pool.id,
        ranking_metric="close",
        hold_count=2,
        rebalance_frequency="daily",
        slippage_bps=15,
        commission_bps=5,
        benchmark_symbol="000300.SH",
        created_by_user_id=user_id,
    )
    session.add(strategy)
    session.commit()
    session.refresh(strategy)

    return strategy.id


@pytest.fixture
def seeded_strategy_id(client, seeded_user, database_url, monkeypatch: pytest.MonkeyPatch) -> str:
    monkeypatch.setenv("OMGTRADER_DATABASE_URL", database_url)

    from app.core.database import SessionLocal

    with SessionLocal() as session:
        return _seed_backtest_inputs(session, user_id=seeded_user["id"])


def test_run_backtest_creates_job_and_metrics(client, auth_headers, seeded_strategy_id: str) -> None:
    response = client.post(
        "/api/backtests/jobs",
        headers=auth_headers,
        json={"strategy_instance_id": seeded_strategy_id},
    )

    assert response.status_code == 201
    assert response.json()["status"] == "completed"
    assert response.json()["metrics"]["total_return"] is not None
