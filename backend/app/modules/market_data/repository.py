from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.modules.market_data.models import DataSourceConfig, DataSyncTask


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
