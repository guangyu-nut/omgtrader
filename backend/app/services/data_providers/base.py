from typing import Protocol


class MarketDataProvider(Protocol):
    def fetch_symbol_bars(self, symbol_code: str) -> dict: ...
