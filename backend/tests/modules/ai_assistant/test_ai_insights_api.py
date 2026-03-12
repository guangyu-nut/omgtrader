def test_generate_ai_insight_persists_result(client, auth_headers, completed_job) -> None:
    response = client.post(f"/api/ai/backtests/{completed_job.id}/insights", headers=auth_headers)

    assert response.status_code == 201
    assert "summary" in response.json()
