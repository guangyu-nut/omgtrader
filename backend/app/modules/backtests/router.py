from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db_session
from app.modules.auth.dependencies import get_current_user
from app.modules.auth.models import User
from app.modules.backtests.repository import BacktestsRepository
from app.modules.backtests.schemas import BacktestJobCreate, BacktestJobRead, BacktestMetricsRead
from app.modules.backtests.service import BacktestsService


router = APIRouter(prefix="/api/backtests", tags=["backtests"])


def get_backtests_service(db_session: Session = Depends(get_db_session)) -> BacktestsService:
    return BacktestsService(BacktestsRepository(db_session))


@router.post("/jobs", response_model=BacktestJobRead, status_code=201)
def run_backtest_job(
    payload: BacktestJobCreate,
    current_user: User = Depends(get_current_user),
    service: BacktestsService = Depends(get_backtests_service),
) -> BacktestJobRead:
    result = service.run_backtest(
        strategy_instance_id=payload.strategy_instance_id,
        current_user_id=current_user.id,
    )
    return BacktestJobRead(
        id=result.job_id,
        status=result.status,
        metrics=BacktestMetricsRead(
            total_return=result.metrics.total_return,
            max_drawdown=result.metrics.max_drawdown,
        ),
    )
