from __future__ import annotations

from fastapi import HTTPException, status

from app.core.security import generate_session_token, verify_password
from app.modules.auth.repository import AuthRepository


class AuthService:
    def __init__(self, repository: AuthRepository) -> None:
        self._repository = repository

    def login(self, username: str, password: str) -> str:
        user = self._repository.get_user_by_username(username)
        if user is None or not verify_password(password, user.password_hash):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

        session = self._repository.create_session(user_id=user.id, token=generate_session_token())
        return session.token
