def test_login_returns_session_token(client, seeded_user) -> None:
    response = client.post("/api/auth/login", json={"username": "demo", "password": "pass123456"})

    assert response.status_code == 200
    assert "token" in response.json()
