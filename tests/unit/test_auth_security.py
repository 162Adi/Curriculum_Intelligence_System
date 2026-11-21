"""
Unit tests for authentication, Argon2id hashing, and JWT tokens.
"""
import pytest
from app.auth.security import (
    verify_password,
    get_password_hash,
    create_access_token,
    create_refresh_token,
    decode_token
)
from app.models.users import Role


def test_argon2_password_hashing():
    raw_password = "Faculty@Secure2026!"
    hashed = get_password_hash(raw_password)

    assert hashed != raw_password
    assert hashed.startswith("$argon2")
    assert verify_password(raw_password, hashed) is True
    assert verify_password("WrongPassword!", hashed) is False


def test_jwt_access_and_refresh_tokens():
    payload = {"sub": "faculty@university.edu", "role": Role.FACULTY.value}
    
    access_token = create_access_token(payload)
    refresh_token = create_refresh_token(payload)

    assert access_token is not None
    assert refresh_token is not None

    decoded_access = decode_token(access_token)
    assert decoded_access["sub"] == "faculty@university.edu"
    assert decoded_access["role"] == "FACULTY"
    assert decoded_access["type"] == "access"

    decoded_refresh = decode_token(refresh_token)
    assert decoded_refresh["sub"] == "faculty@university.edu"
    assert decoded_refresh["type"] == "refresh"


def test_invalid_token_decoding():
    with pytest.raises(Exception):
        decode_token("invalid.malformed.jwt.token")
