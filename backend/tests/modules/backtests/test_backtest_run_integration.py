from __future__ import annotations

from datetime import UTC, date, datetime

from sqlalchemy import select

from app.modules.auth.models import User
from app.modules.backtests.models import BacktestJob
from app.modules.backtests.repository import BacktestsRepository
from app.modules.backtests.service import BacktestsService
from app.modules.market_data.models import BarDaily, BarMinute, Symbol
from app.modules.results.models import BacktestMetric
from app.modules.strategies.models import StockPool, StrategyInstance


def _seed_backtest_inputs(session, *, user_id: str) -> str:
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


def test_run_backtest_persists_job_and_metrics(db_session) -> None:
    user = User(username="backtest-demo", password_hash="hashed")
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    strategy_id = _seed_backtest_inputs(db_session, user_id=user.id)
    service = BacktestsService(BacktestsRepository(db_session))

    result = service.run_backtest(strategy_instance_id=strategy_id)
    job = db_session.get(BacktestJob, result.job_id)
    metric = db_session.execute(
        select(BacktestMetric).where(BacktestMetric.backtest_job_id == result.job_id)
    ).scalar_one()

    assert result.status == "completed"
    assert job is not None
    assert metric.total_return == result.metrics.total_return
    assert metric.max_drawdown == result.metrics.max_drawdown
