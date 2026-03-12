def test_get_backtest_result_returns_curve_and_metrics(client, auth_headers, completed_job) -> None:
    response = client.get(f"/api/results/backtests/{completed_job.id}", headers=auth_headers)

    assert response.status_code == 200
    assert response.json()["metrics"]["max_drawdown"] is not None
    assert len(response.json()["equity_curve"]) > 0
