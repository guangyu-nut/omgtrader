def test_list_sync_tasks_returns_empty_collection(client, auth_headers) -> None:
    response = client.get("/api/market-data/sync-tasks", headers=auth_headers)

    assert response.status_code == 200
    assert response.json() == []
