from __future__ import annotations

from datetime import UTC, date, datetime

from app.core.database import SessionLocal
from app.core.security import hash_password
from app.modules.auth.models import User
from app.modules.market_data.models import BarDaily, BarMinute, DataCoverage, Symbol


def _ensure_user(session) -> User:
    user = session.query(User).filter_by(username="demo").first()
    if user is None:
        user = User(username="demo", password_hash=hash_password("pass123456"))
        session.add(user)
        session.commit()
        session.refresh(user)

    return user


def _ensure_symbol(session, *, code: str, name: str, market: str) -> Symbol:
    symbol = session.query(Symbol).filter_by(code=code).first()
    if symbol is None:
        symbol = Symbol(code=code, name=name, market=market)
        session.add(symbol)
        session.commit()
        session.refresh(symbol)

    return symbol


def _ensure_daily_bar(session, *, symbol_id: str, trade_date: date, open: float, high: float, low: float, close: float, volume: float) -> None:
    existing = session.query(BarDaily).filter_by(symbol_id=symbol_id, trade_date=trade_date).first()
    if existing is None:
        session.add(
            BarDaily(
                symbol_id=symbol_id,
                trade_date=trade_date,
                open=open,
                high=high,
                low=low,
                close=close,
                volume=volume,
            )
        )
        session.commit()


def _ensure_minute_bar(
    session,
    *,
    symbol_id: str,
    bar_time: datetime,
    open: float,
    high: float,
    low: float,
    close: float,
    volume: float,
) -> None:
    existing = session.query(BarMinute).filter_by(symbol_id=symbol_id, bar_time=bar_time).first()
    if existing is None:
        session.add(
            BarMinute(
                symbol_id=symbol_id,
                bar_time=bar_time,
                open=open,
                high=high,
                low=low,
                close=close,
                volume=volume,
            )
        )
        session.commit()


def main() -> None:
    with SessionLocal() as session:
        _ensure_user(session)

        symbols = [
            _ensure_symbol(session, code="000001.SZ", name="Ping An Bank", market="SZ"),
            _ensure_symbol(session, code="600000.SH", name="Shanghai Bank", market="SH"),
            _ensure_symbol(session, code="000002.SZ", name="Vanke", market="SZ"),
        ]

        daily_bars = {
            "000001.SZ": {"open": 10.0, "high": 10.4, "low": 9.9, "close": 10.2, "volume": 120_000},
            "600000.SH": {"open": 12.0, "high": 12.5, "low": 11.9, "close": 12.3, "volume": 110_000},
            "000002.SZ": {"open": 9.5, "high": 9.7, "low": 9.4, "close": 9.6, "volume": 90_000},
        }
        minute_bars = {
            "000001.SZ": {"open": 10.05, "high": 10.2, "low": 10.0, "close": 10.2, "volume": 15_000},
            "600000.SH": {"open": 12.05, "high": 12.3, "low": 12.0, "close": 12.3, "volume": 16_000},
            "000002.SZ": {"open": 9.55, "high": 9.7, "low": 9.5, "close": 9.6, "volume": 14_000},
        }

        for symbol in symbols:
            _ensure_daily_bar(
                session,
                symbol_id=symbol.id,
                trade_date=date(2025, 1, 3),
                **daily_bars[symbol.code],
            )
            _ensure_minute_bar(
                session,
                symbol_id=symbol.id,
                bar_time=datetime(2025, 1, 6, 9, 31, tzinfo=UTC),
                **minute_bars[symbol.code],
            )
            coverage = session.query(DataCoverage).filter_by(symbol_code=symbol.code).first()
            if coverage is None:
                coverage = DataCoverage(symbol_code=symbol.code)
                session.add(coverage)

            coverage.daily_start = date(2025, 1, 3)
            coverage.daily_end = date(2025, 1, 3)
            coverage.minute_start = datetime(2025, 1, 6, 9, 31, tzinfo=UTC)
            coverage.minute_end = datetime(2025, 1, 6, 9, 31, tzinfo=UTC)

        session.commit()


if __name__ == "__main__":
    main()
