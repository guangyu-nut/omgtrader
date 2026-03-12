from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db_session
from app.modules.auth.dependencies import get_current_user
from app.modules.auth.models import User
from app.modules.results.repository import ResultsRepository
from app.modules.results.schemas import BacktestResultDetail
from app.modules.results.service import ResultsService


router = APIRouter(prefix="/api/results", tags=["results"])


def get_results_service(db_session: Session = Depends(get_db_session)) -> ResultsService:
    return ResultsService(ResultsRepository(db_session))


@router.get("/backtests/{job_id}", response_model=BacktestResultDetail)
def get_backtest_result(
    job_id: str,
    current_user: User = Depends(get_current_user),
    service: ResultsService = Depends(get_results_service),
) -> BacktestResultDetail:
    return service.get_backtest_result(job_id=job_id, current_user_id=current_user.id)
