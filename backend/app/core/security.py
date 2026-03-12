from __future__ import annotations

import hashlib
import hmac
import secrets


def hash_password(password: str, salt: str | None = None) -> str:
    actual_salt = salt or secrets.token_hex(8)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), actual_salt.encode("utf-8"), 120_000)
    return f"pbkdf2_sha256${actual_salt}${digest.hex()}"


def verify_password(password: str, password_hash: str) -> bool:
    algorithm, salt, expected = password_hash.split("$", maxsplit=2)
    if algorithm != "pbkdf2_sha256":
        return False

    candidate = hash_password(password, salt=salt)
    return hmac.compare_digest(candidate, password_hash)


def generate_session_token() -> str:
    return secrets.token_urlsafe(32)
