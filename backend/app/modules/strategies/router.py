from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db_session
from app.modules.auth.dependencies import get_current_user
from app.modules.auth.models import User
from app.modules.strategies.repository import StrategiesRepository
from app.modules.strategies.schemas import StockPoolCreate, StockPoolRead, StrategyInstanceCreate, StrategyInstanceRead
from app.modules.strategies.service import StrategiesService


router = APIRouter(prefix="/api/strategies", tags=["strategies"])


def get_strategies_service(db_session: Session = Depends(get_db_session)) -> StrategiesService:
    return StrategiesService(StrategiesRepository(db_session))


@router.post("/stock-pools", response_model=StockPoolRead, status_code=201)
def create_stock_pool(
    payload: StockPoolCreate,
    current_user: User = Depends(get_current_user),
    service: StrategiesService = Depends(get_strategies_service),
) -> StockPoolRead:
    return service.create_stock_pool(payload, current_user)


@router.post("/strategy-instances", response_model=StrategyInstanceRead, status_code=201)
def create_strategy_instance(
    payload: StrategyInstanceCreate,
    current_user: User = Depends(get_current_user),
    service: StrategiesService = Depends(get_strategies_service),
) -> StrategyInstanceRead:
    return service.create_strategy_instance(payload, current_user)
