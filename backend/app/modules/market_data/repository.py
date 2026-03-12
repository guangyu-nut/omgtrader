from __future__ import annotations

from datetime import UTC, datetime

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.modules.market_data.models import BarDaily, BarMinute, DataCoverage, DataSourceConfig, DataSyncTask, Symbol


class MarketDataRepository:
    def __init__(self, db_session: Session) -> None:
        self._db_session = db_session

    def create_data_source(self, *, name: str, provider_type: str, enabled: bool, created_by_user_id: str) -> DataSourceConfig:
        data_source = DataSourceConfig(
            name=name,
            provider_type=provider_type,
            enabled=enabled,
            created_by_user_id=created_by_user_id,
        )
        self._db_session.add(data_source)
        self._db_session.commit()
        self._db_session.refresh(data_source)
        return data_source

    def list_sync_tasks(self) -> list[DataSyncTask]:
        statement = select(DataSyncTask).order_by(DataSyncTask.started_at.desc())
        return list(self._db_session.scalars(statement))

    def get_symbol_by_code(self, symbol_code: str) -> Symbol | None:
        statement = select(Symbol).where(Symbol.code == symbol_code)
        return self._db_session.scalar(statement)

    def add_daily_bars(self, symbol_id: str, daily_bars: list[dict]) -> int:
        for bar in daily_bars:
            self._db_session.add(BarDaily(symbol_id=symbol_id, **bar))
        self._db_session.commit()
        return len(daily_bars)

    def add_minute_bars(self, symbol_id: str, minute_bars: list[dict]) -> int:
        for bar in minute_bars:
            self._db_session.add(BarMinute(symbol_id=symbol_id, **bar))
        self._db_session.commit()
        return len(minute_bars)

    def upsert_coverage(self, symbol_code: str, *, daily_start, daily_end, minute_start, minute_end) -> DataCoverage:
        statement = select(DataCoverage).where(DataCoverage.symbol_code == symbol_code)
        coverage = self._db_session.scalar(statement)
        if coverage is None:
            coverage = DataCoverage(symbol_code=symbol_code)
            self._db_session.add(coverage)

        coverage.daily_start = daily_start
        coverage.daily_end = daily_end
        coverage.minute_start = minute_start
        coverage.minute_end = minute_end
        coverage.updated_at = datetime.now(UTC)

        self._db_session.commit()
        self._db_session.refresh(coverage)
        return coverage

    def list_coverages(self) -> list[DataCoverage]:
        statement = select(DataCoverage).order_by(DataCoverage.symbol_code.asc())
        return list(self._db_session.scalars(statement))
