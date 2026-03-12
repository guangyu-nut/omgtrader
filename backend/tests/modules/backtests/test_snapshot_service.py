from __future__ import annotations

from app.modules.auth.models import User
from app.modules.backtests.repository import BacktestsRepository
from app.modules.backtests.service import BacktestsService
from app.modules.strategies.models import StockPool, StrategyInstance


def test_create_snapshot_freezes_strategy_and_stock_pool_inputs(db_session) -> None:
    user = User(username="snapshot-demo", password_hash="hashed")
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    stock_pool = StockPool(
        name="CSI300 manual",
        input_mode="manual",
        symbols=["000001.SZ", "600000.SH"],
        created_by_user_id=user.id,
    )
    db_session.add(stock_pool)
    db_session.commit()
    db_session.refresh(stock_pool)

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
        created_by_user_id=user.id,
    )
    db_session.add(strategy)
    db_session.commit()
    db_session.refresh(strategy)

    service = BacktestsService(BacktestsRepository(db_session))
    snapshot = service.create_snapshot(strategy_instance_id=strategy.id)

    strategy.hold_count = 4
    stock_pool.symbols = ["000002.SZ"]

    assert snapshot.strategy_instance_id == strategy.id
    assert snapshot.hold_count == 2
    assert snapshot.stock_pool_symbols == ("000001.SZ", "600000.SH")
    assert snapshot.data_version == "latest"
