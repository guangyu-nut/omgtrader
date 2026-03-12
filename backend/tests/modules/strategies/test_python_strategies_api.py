from __future__ import annotations

import hashlib

from app.core.database import SessionLocal
from app.modules.auth.models import User


def _hash_password(password: str, salt: str = "testsalt") -> str:
    digest = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt.encode("utf-8"), 120_000)
    return f"pbkdf2_sha256${salt}${digest.hex()}"


def _create_user(username: str, password: str = "pass123456") -> User:
    with SessionLocal() as session:
        user = User(username=username, password_hash=_hash_password(password))
        session.add(user)
        session.commit()
        session.refresh(user)
        return user


def _create_python_strategy(client, auth_headers, *, name: str) -> dict:
    response = client.post(
        "/api/strategies/python",
        headers=auth_headers,
        json={
            "name": name,
            "description": f"{name} description",
            "tags": ["轮动", "Python"],
            "parameter_schema_text": "window: int",
            "code": "class Strategy:\n    pass\n",
        },
    )

    assert response.status_code == 201
    return response.json()


def test_create_list_and_get_python_strategies(client, auth_headers) -> None:
    first = _create_python_strategy(client, auth_headers, name="Alpha Strategy")
    second = _create_python_strategy(client, auth_headers, name="Beta Strategy")

    list_response = client.get("/api/strategies/python", headers=auth_headers)
    detail_response = client.get(f"/api/strategies/python/{first['id']}", headers=auth_headers)

    assert list_response.status_code == 200
    assert [item["id"] for item in list_response.json()] == [second["id"], first["id"]]
    assert detail_response.status_code == 200
    assert detail_response.json()["tags"] == ["轮动", "Python"]
    assert detail_response.json()["code"] == "class Strategy:\n    pass\n"


def test_update_and_delete_python_strategy(client, auth_headers) -> None:
    created = _create_python_strategy(client, auth_headers, name="Draft Strategy")

    update_response = client.put(
        f"/api/strategies/python/{created['id']}",
        headers=auth_headers,
        json={
            "name": "Momentum Draft",
            "description": "Updated description",
            "tags": ["动量"],
            "parameter_schema_text": "lookback: int",
            "code": "print('updated')\n",
        },
    )
    delete_response = client.delete(f"/api/strategies/python/{created['id']}", headers=auth_headers)
    missing_response = client.get(f"/api/strategies/python/{created['id']}", headers=auth_headers)

    assert update_response.status_code == 200
    assert update_response.json()["name"] == "Momentum Draft"
    assert update_response.json()["tags"] == ["动量"]
    assert delete_response.status_code == 204
    assert missing_response.status_code == 404


def test_python_strategy_validation_rejects_blank_name_and_code(client, auth_headers) -> None:
    response = client.post(
        "/api/strategies/python",
        headers=auth_headers,
        json={
            "name": "",
            "description": "",
            "tags": [],
            "parameter_schema_text": "",
            "code": "",
        },
    )

    assert response.status_code == 422


def test_python_strategy_is_hidden_from_other_users(client, auth_headers) -> None:
    created = _create_python_strategy(client, auth_headers, name="Private Strategy")
    _create_user("other-user", "pass123456")

    login_response = client.post("/api/auth/login", json={"username": "other-user", "password": "pass123456"})
    other_headers = {"Authorization": f"Bearer {login_response.json()['token']}"}

    detail_response = client.get(f"/api/strategies/python/{created['id']}", headers=other_headers)

    assert detail_response.status_code == 404
