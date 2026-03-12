from __future__ import annotations

import hashlib
import os
from pathlib import Path
from types import SimpleNamespace
from datetime import UTC, date, datetime

import pytest
from alembic import command
from alembic.config import Config
from fastapi.testclient import TestClient


def _hash_password(password: str, salt: str = "testsalt") -> str:
    digest = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt.encode("utf-8"), 120_000)
    return f"pbkdf2_sha256${salt}${digest.hex()}"


@pytest.fixture
def database_url(tmp_path: Path) -> str:
    return f"sqlite:///{tmp_path / 'test.db'}"


@pytest.fixture
def client(monkeypatch: pytest.MonkeyPatch, database_url: str) -> TestClient:
    monkeypatch.setenv("OMGTRADER_DATABASE_URL", database_url)

    from app.core.config import get_settings
    from app.core.database import reset_database_state

    get_settings.cache_clear()
    reset_database_state()

    alembic_config = Config("backend/alembic.ini")
    alembic_config.set_main_option("sqlalchemy.url", database_url)
    command.upgrade(alembic_config, "head")

    from app.main import app

    with TestClient(app) as test_client:
        yield test_client

    reset_database_state()
    get_settings.cache_clear()


@pytest.fixture
def seeded_user(database_url: str, monkeypatch: pytest.MonkeyPatch) -> dict[str, str]:
    monkeypatch.setenv("OMGTRADER_DATABASE_URL", database_url)

    from app.core.config import get_settings
    from app.core.database import SessionLocal, reset_database_state
    from app.modules.auth.models import User

    get_settings.cache_clear()
    reset_database_state()

    with SessionLocal() as session:
        user = User(username="demo", password_hash=_hash_password("pass123456"))
        session.add(user)
        session.commit()
        session.refresh(user)

        return {"id": user.id, "username": user.username}


@pytest.fixture
def auth_headers(client: TestClient, seeded_user: dict[str, str]) -> dict[str, str]:
    response = client.post("/api/auth/login", json={"username": "demo", "password": "pass123456"})
    token = response.json()["token"]
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def db_session(database_url: str, monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setenv("OMGTRADER_DATABASE_URL", database_url)

    from app.core.config import get_settings
    from app.core.database import SessionLocal, reset_database_state

    get_settings.cache_clear()
    reset_database_state()

    alembic_config = Config("backend/alembic.ini")
    alembic_config.set_main_option("sqlalchemy.url", database_url)
    command.upgrade(alembic_config, "head")

    with SessionLocal() as session:
        yield session


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
def completed_job(client: TestClient, seeded_user: dict[str, str], database_url: str, monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setenv("OMGTRADER_DATABASE_URL", database_url)

    from app.core.database import SessionLocal
    from app.modules.backtests.repository import BacktestsRepository
    from app.modules.backtests.service import BacktestsService

    with SessionLocal() as session:
        strategy_id = _seed_backtest_inputs(session, user_id=seeded_user["id"])
        result = BacktestsService(BacktestsRepository(session)).run_backtest(
            strategy_instance_id=strategy_id,
            current_user_id=seeded_user["id"],
        )

    return SimpleNamespace(id=result.job_id, strategy_instance_id=strategy_id)
