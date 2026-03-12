from __future__ import annotations

from dataclasses import dataclass

from sqlalchemy.orm import Session

from app.modules.market_data.repository import MarketDataRepository
from app.modules.market_data.validators import MarketDataValidator


@dataclass
class IngestionResult:
    daily_rows: int
    minute_rows: int
    coverage: object


class MarketDataIngestionService:
    def __init__(self, db_session: Session) -> None:
        self._repository = MarketDataRepository(db_session)
        self._validator = MarketDataValidator()

    def sync_symbol_bars(self, symbol_code: str, provider) -> IngestionResult:
        symbol = self._repository.get_symbol_by_code(symbol_code)
        if symbol is None:
            raise ValueError(f"Unknown symbol: {symbol_code}")

        payload = provider.fetch_symbol_bars(symbol_code)
        daily_bars = payload["daily_bars"]
        minute_bars = payload["minute_bars"]

        self._validator.assert_no_duplicate_timestamps(minute_bars)

        daily_rows = self._repository.add_daily_bars(symbol.id, daily_bars)
        minute_rows = self._repository.add_minute_bars(symbol.id, minute_bars)
        coverage = self._repository.upsert_coverage(
            symbol_code,
            daily_start=min(bar["trade_date"] for bar in daily_bars),
            daily_end=max(bar["trade_date"] for bar in daily_bars),
            minute_start=min(bar["bar_time"] for bar in minute_bars),
            minute_end=max(bar["bar_time"] for bar in minute_bars),
        )

        return IngestionResult(daily_rows=daily_rows, minute_rows=minute_rows, coverage=coverage)
