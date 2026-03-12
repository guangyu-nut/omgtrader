from collections.abc import Iterator

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from app.core.config import get_settings


class Base(DeclarativeBase):
    pass


_engine = None
_session_factory = None


def _build_engine():
    settings = get_settings()
    connect_args = {"check_same_thread": False} if settings.database_url.startswith("sqlite") else {}
    return create_engine(settings.database_url, future=True, connect_args=connect_args)


def get_engine():
    global _engine

    if _engine is None:
        _engine = _build_engine()

    return _engine


def get_session_factory():
    global _session_factory

    if _session_factory is None:
        _session_factory = sessionmaker(bind=get_engine(), autoflush=False, autocommit=False)

    return _session_factory


def get_db_session() -> Iterator[Session]:
    with get_session_factory()() as session:
        yield session


def reset_database_state() -> None:
    global _engine, _session_factory

    if _engine is not None:
        _engine.dispose()

    _engine = None
    _session_factory = None


def SessionLocal() -> Session:
    return get_session_factory()()
