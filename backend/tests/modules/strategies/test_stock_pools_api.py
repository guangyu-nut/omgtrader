def test_create_stock_pool_with_manual_symbols(client, auth_headers) -> None:
    response = client.post(
        "/api/strategies/stock-pools",
        headers=auth_headers,
        json={"name": "CSI300 manual", "input_mode": "manual", "symbols": ["000001.SZ", "600000.SH"]},
    )

    assert response.status_code == 201
    assert response.json()["symbols"] == ["000001.SZ", "600000.SH"]
