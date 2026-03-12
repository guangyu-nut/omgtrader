from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db_session
from app.modules.auth.dependencies import get_current_user
from app.modules.auth.models import User
from app.modules.market_data.repository import MarketDataRepository
from app.modules.market_data.schemas import DataCoverageRead, DataSourceCreate, DataSourceRead, DataSyncTaskRead
from app.modules.market_data.service import MarketDataService


router = APIRouter(prefix="/api/market-data", tags=["market-data"])


def get_market_data_service(db_session: Session = Depends(get_db_session)) -> MarketDataService:
    return MarketDataService(MarketDataRepository(db_session))


@router.post("/data-sources", response_model=DataSourceRead, status_code=201)
def create_data_source(
    payload: DataSourceCreate,
    current_user: User = Depends(get_current_user),
    service: MarketDataService = Depends(get_market_data_service),
) -> DataSourceRead:
    return service.create_data_source(payload, current_user)


@router.get("/sync-tasks", response_model=list[DataSyncTaskRead])
def list_sync_tasks(
    _: User = Depends(get_current_user),
    service: MarketDataService = Depends(get_market_data_service),
) -> list[DataSyncTaskRead]:
    return service.list_sync_tasks()


@router.get("/coverage", response_model=list[DataCoverageRead])
def list_coverages(
    _: User = Depends(get_current_user),
    service: MarketDataService = Depends(get_market_data_service),
) -> list[DataCoverageRead]:
    return service.list_coverages()
