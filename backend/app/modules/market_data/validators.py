from __future__ import annotations


class MarketDataValidator:
    def assert_no_duplicate_timestamps(self, minute_bars: list[dict]) -> None:
        timestamps = [bar["bar_time"] for bar in minute_bars]
        if len(timestamps) != len(set(timestamps)):
            raise ValueError("Duplicate minute bar timestamps detected")
