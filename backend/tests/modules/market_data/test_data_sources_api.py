def test_create_data_source_config(client, auth_headers) -> None:
    response = client.post(
        "/api/market-data/data-sources",
        headers=auth_headers,
        json={"name": "free-default", "provider_type": "free", "enabled": True},
    )

    assert response.status_code == 201
    assert response.json()["provider_type"] == "free"
