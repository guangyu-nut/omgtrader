from __future__ import annotations

from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session

from app.core.database import get_db_session
from app.modules.auth.dependencies import get_current_user
from app.modules.auth.models import User
from app.modules.strategies.repository import StrategiesRepository
from app.modules.strategies.schemas import (
    PythonStrategyCreate,
    PythonStrategyListItem,
    PythonStrategyRead,
    PythonStrategyUpdate,
    StockPoolCreate,
    StockPoolRead,
    StrategyInstanceCreate,
    StrategyInstanceRead,
)
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


@router.get("/python", response_model=list[PythonStrategyListItem])
def list_python_strategies(
    current_user: User = Depends(get_current_user),
    service: StrategiesService = Depends(get_strategies_service),
) -> list[PythonStrategyListItem]:
    return service.list_python_strategies(current_user)


@router.get("/python/{strategy_id}", response_model=PythonStrategyRead)
def get_python_strategy(
    strategy_id: str,
    current_user: User = Depends(get_current_user),
    service: StrategiesService = Depends(get_strategies_service),
) -> PythonStrategyRead:
    return service.get_python_strategy(strategy_id, current_user)


@router.post("/python", response_model=PythonStrategyRead, status_code=201)
def create_python_strategy(
    payload: PythonStrategyCreate,
    current_user: User = Depends(get_current_user),
    service: StrategiesService = Depends(get_strategies_service),
) -> PythonStrategyRead:
    return service.create_python_strategy(payload, current_user)


@router.put("/python/{strategy_id}", response_model=PythonStrategyRead)
def update_python_strategy(
    strategy_id: str,
    payload: PythonStrategyUpdate,
    current_user: User = Depends(get_current_user),
    service: StrategiesService = Depends(get_strategies_service),
) -> PythonStrategyRead:
    return service.update_python_strategy(strategy_id, payload, current_user)


@router.delete("/python/{strategy_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_python_strategy(
    strategy_id: str,
    current_user: User = Depends(get_current_user),
    service: StrategiesService = Depends(get_strategies_service),
) -> Response:
    service.delete_python_strategy(strategy_id, current_user)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
