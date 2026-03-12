from __future__ import annotations

from datetime import UTC, date, datetime

from app.core.database import SessionLocal
from app.modules.market_data.models import DataCoverage, Symbol


def main() -> None:
    with SessionLocal() as session:
        if session.query(Symbol).filter_by(code="000001.SZ").first() is None:
            session.add(Symbol(code="000001.SZ", name="Ping An Bank", market="SZ"))

        if session.query(DataCoverage).filter_by(symbol_code="000001.SZ").first() is None:
            session.add(
                DataCoverage(
                    symbol_code="000001.SZ",
                    daily_start=date(2025, 1, 2),
                    daily_end=date(2025, 1, 3),
                    minute_start=datetime(2025, 1, 6, 9, 31, tzinfo=UTC),
                    minute_end=datetime(2025, 1, 6, 9, 32, tzinfo=UTC),
                )
            )

        session.commit()


if __name__ == "__main__":
    main()
