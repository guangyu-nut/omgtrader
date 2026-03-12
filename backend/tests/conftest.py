from __future__ import annotations

import hashlib
import os
from pathlib import Path

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
