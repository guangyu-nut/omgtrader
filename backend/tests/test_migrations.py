import os
from pathlib import Path

from alembic import command
from alembic.config import Config
from sqlalchemy import create_engine, inspect


def test_initial_migration_creates_core_tables(tmp_path: Path) -> None:
    database_url = f"sqlite:///{tmp_path / 'test.db'}"
    alembic_config = Config("backend/alembic.ini")
    alembic_config.set_main_option("sqlalchemy.url", database_url)

    previous_database_url = os.environ.get("OMGTRADER_DATABASE_URL")
    os.environ["OMGTRADER_DATABASE_URL"] = database_url
    try:
        command.upgrade(alembic_config, "head")
    finally:
        if previous_database_url is None:
            os.environ.pop("OMGTRADER_DATABASE_URL", None)
        else:
            os.environ["OMGTRADER_DATABASE_URL"] = previous_database_url

    engine = create_engine(database_url)
    tables = set(inspect(engine).get_table_names())

    assert {"users", "symbols", "bar_daily", "bar_minute", "strategy_instances", "backtest_jobs"} <= tables
