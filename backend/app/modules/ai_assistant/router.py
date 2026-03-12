from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db_session
from app.modules.ai_assistant.repository import AiAssistantRepository
from app.modules.ai_assistant.schemas import AiInsightRead
from app.modules.ai_assistant.service import AiAssistantService
from app.modules.auth.dependencies import get_current_user
from app.modules.auth.models import User


router = APIRouter(prefix="/api/ai", tags=["ai-assistant"])


def get_ai_assistant_service(db_session: Session = Depends(get_db_session)) -> AiAssistantService:
    return AiAssistantService(AiAssistantRepository(db_session))


@router.post("/backtests/{job_id}/insights", response_model=AiInsightRead, status_code=201)
def generate_backtest_insight(
    job_id: str,
    current_user: User = Depends(get_current_user),
    service: AiAssistantService = Depends(get_ai_assistant_service),
) -> AiInsightRead:
    return service.generate_backtest_insight(job_id=job_id, current_user_id=current_user.id)
