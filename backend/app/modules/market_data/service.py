from __future__ import annotations

from app.modules.auth.models import User
from app.modules.market_data.repository import MarketDataRepository
from app.modules.market_data.schemas import DataSourceCreate


class MarketDataService:
    def __init__(self, repository: MarketDataRepository) -> None:
        self._repository = repository

    def create_data_source(self, payload: DataSourceCreate, current_user: User):
        return self._repository.create_data_source(
            name=payload.name,
            provider_type=payload.provider_type,
            enabled=payload.enabled,
            created_by_user_id=current_user.id,
        )

    def list_sync_tasks(self):
        return self._repository.list_sync_tasks()

    def list_coverages(self):
        return self._repository.list_coverages()
