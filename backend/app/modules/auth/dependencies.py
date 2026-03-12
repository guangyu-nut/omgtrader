from __future__ import annotations

from typing import Annotated

from fastapi import Depends, Header, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db_session
from app.modules.auth.models import User
from app.modules.auth.repository import AuthRepository


def get_current_user(
    authorization: Annotated[str | None, Header()] = None,
    db_session: Session = Depends(get_db_session),
) -> User:
    if authorization is None or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing authorization token")

    token = authorization.removeprefix("Bearer ").strip()
    user = AuthRepository(db_session).get_user_by_token(token)
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid session token")

    return user
