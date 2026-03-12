from __future__ import annotations

from datetime import UTC, date, datetime

from app.modules.market_data.models import Symbol
from app.modules.market_data.ingestion import MarketDataIngestionService


class FakeProvider:
    def fetch_symbol_bars(self, symbol_code: str):
        return {
            "daily_bars": [
                {
                    "close": 10.3,
                    "high": 10.5,
                    "low": 9.9,
                    "open": 10.0,
                    "trade_date": date(2025, 1, 3),
                    "volume": 100_000,
                }
            ],
            "minute_bars": [
                {
                    "bar_time": datetime(2025, 1, 6, 9, 31, tzinfo=UTC),
                    "close": 10.35,
                    "high": 10.4,
                    "low": 10.1,
                    "open": 10.2,
                    "volume": 10_000,
                },
                {
                    "bar_time": datetime(2025, 1, 6, 9, 32, tzinfo=UTC),
                    "close": 10.36,
                    "high": 10.42,
                    "low": 10.21,
                    "open": 10.31,
                    "volume": 11_000,
                },
            ],
        }


def test_sync_daily_and_minute_bars_updates_coverage(db_session) -> None:
    db_session.add(Symbol(code="000001.SZ", name="Ping An Bank", market="SZ"))
    db_session.commit()

    service = MarketDataIngestionService(db_session)
    result = service.sync_symbol_bars(symbol_code="000001.SZ", provider=FakeProvider())

    assert result.daily_rows > 0
    assert result.minute_rows > 0
    assert result.coverage.symbol_code == "000001.SZ"
