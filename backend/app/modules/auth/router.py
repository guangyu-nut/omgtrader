from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db_session
from app.modules.auth.repository import AuthRepository
from app.modules.auth.schemas import LoginRequest, LoginResponse
from app.modules.auth.service import AuthService


router = APIRouter(prefix="/api/auth", tags=["auth"])


def get_auth_service(db_session: Session = Depends(get_db_session)) -> AuthService:
    return AuthService(AuthRepository(db_session))


@router.post("/login", response_model=LoginResponse)
def login(payload: LoginRequest, service: AuthService = Depends(get_auth_service)) -> LoginResponse:
    return LoginResponse(token=service.login(payload.username, payload.password))
