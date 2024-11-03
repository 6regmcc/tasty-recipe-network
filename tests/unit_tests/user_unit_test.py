import os
from datetime import timedelta

import jwt

from tasty_recipe_network.routes.user_auth_routes import (
    pwd_context,
    verify_password,
    get_password_hash,
    authenticate_user,
    create_access_token,
)
from tasty_recipe_network.schemas.user_schema import Return_User_With_Pwd
from tasty_recipe_network.config import ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM


def mock_output(return_value=None):
    return lambda *args, **kwargs: return_value


def test_verify_password_success():
    password = "Password1"
    hashed_password = pwd_context.hash("Password1")
    assert verify_password(plain_password=password, hashed_password=hashed_password)


def test_verify_password_failure():
    password = "abc123"
    hashed_password = pwd_context.hash("Password1")
    assert (
        verify_password(plain_password=password, hashed_password=hashed_password)
        is False
    )


# authenticate_user


def test_authenticate_user_success(monkeypatch, db_session):
    returned_user = Return_User_With_Pwd(
        username="test@email.com",
        password=get_password_hash("Password1"),
        first_name="Tom",
        last_name="Smith",
        user_id=12345,
    )

    monkeypatch.setattr(
        "tasty_recipe_network.routes.user_auth_routes.db_get_user_by_username",
        mock_output(returned_user),
    )
    user = authenticate_user(
        username="test@email.com", password="Password1", db=db_session
    )
    assert user
    assert isinstance(user, Return_User_With_Pwd)


def test_authenticate_user_failure(monkeypatch, db_session):
    returned_user = Return_User_With_Pwd(
        username="test@email.com",
        password=get_password_hash("Password1"),
        first_name="Tom",
        last_name="Smith",
        user_id=12345,
    )

    monkeypatch.setattr(
        "tasty_recipe_network.routes.user_auth_routes.db_get_user_by_username",
        mock_output(returned_user),
    )
    user = authenticate_user(
        username="test@email.com", password="Password2", db=db_session
    )
    assert user is None


def test_get_password_hash():
    password = "Password1"
    hashed_password = get_password_hash(password)
    assert pwd_context.verify(password, hashed_password)


def test_create_access_token():
    data = {"sub": "tom@email.com"}
    token = create_access_token(
        data=data, expires_delta=timedelta(minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES))
    )
    assert token
    payload = jwt.decode(token, os.getenv("SECRET_KEY"), algorithms=[ALGORITHM])
    username: str = payload.get("sub")
    assert username == data["sub"]


# create_access_token


# get_current_user


# get_current_user
