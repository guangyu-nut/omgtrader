def test_create_strategy_instance_for_top_n_equal_weight(client, auth_headers) -> None:
    stock_pool_response = client.post(
        "/api/strategies/stock-pools",
        headers=auth_headers,
        json={"name": "CSI300 manual", "input_mode": "manual", "symbols": ["000001.SZ", "600000.SH"]},
    )

    response = client.post(
        "/api/strategies/strategy-instances",
        headers=auth_headers,
        json={
            "name": "Top N demo",
            "template_type": "top_n_equal_weight",
            "stock_pool_id": stock_pool_response.json()["id"],
            "ranking_metric": "close",
            "hold_count": 2,
            "rebalance_frequency": "daily",
            "slippage_bps": 15,
            "commission_bps": 5,
            "benchmark_symbol": "000300.SH",
        },
    )

    assert response.status_code == 201
    assert response.json()["template_type"] == "top_n_equal_weight"
    assert response.json()["stock_pool_id"] == stock_pool_response.json()["id"]
