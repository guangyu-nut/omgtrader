from __future__ import annotations

from datetime import UTC, date, datetime

from app.modules.market_data.models import DataCoverage


def test_get_data_coverage_returns_symbol_rows(client, auth_headers, db_session) -> None:
    db_session.add(
        DataCoverage(
            symbol_code="000001.SZ",
            daily_end=date(2025, 1, 3),
            daily_start=date(2025, 1, 2),
            minute_end=datetime(2025, 1, 6, 9, 32, tzinfo=UTC),
            minute_start=datetime(2025, 1, 6, 9, 31, tzinfo=UTC),
        )
    )
    db_session.commit()

    response = client.get("/api/market-data/coverage", headers=auth_headers)

    assert response.status_code == 200
    assert response.json()[0]["symbol_code"] == "000001.SZ"
