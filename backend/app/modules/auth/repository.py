from __future__ import annotations

from datetime import UTC, datetime, timedelta

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.modules.auth.models import Session as UserSession
from app.modules.auth.models import User


class AuthRepository:
    def __init__(self, db_session: Session) -> None:
        self._db_session = db_session

    def get_user_by_username(self, username: str) -> User | None:
        statement = select(User).where(User.username == username)
        return self._db_session.scalar(statement)

    def create_session(self, user_id: str, token: str) -> UserSession:
        session = UserSession(
            user_id=user_id,
            token=token,
            created_at=datetime.now(UTC),
            expires_at=datetime.now(UTC) + timedelta(days=7),
        )
        self._db_session.add(session)
        self._db_session.commit()
        self._db_session.refresh(session)
        return session

    def get_user_by_token(self, token: str) -> User | None:
        statement = (
            select(User)
            .join(UserSession, UserSession.user_id == User.id)
            .where(UserSession.token == token, UserSession.expires_at >= datetime.now(UTC))
        )
        return self._db_session.scalar(statement)
