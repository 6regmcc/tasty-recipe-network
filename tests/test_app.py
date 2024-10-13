import pytest
from fastapi.testclient import TestClient

from app.main import app
from schemas.user_schema import Notes_Schema_response
from tests.database.db_database_connection import db_create_all, db_drop_all





def test_first(test_client):
    response = test_client.get('/')
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}


def test_create_user(test_client):
    body = {
        "username": "tddom@email.com",
        "password": "Password1",
        "first_name": "Tom",
        "last_name": "Smith"
    }

    response = test_client.post("/user/create_user", json=body)
    assert response.status_code == 200
    data = response.json()
    assert "user_id" in data
    assert "username" in data
    assert "password" not in data
    assert "first_name" in data
    assert "last_name" in data



"""
def test_create_note_success(test_client):
    body = {"test_note": 'first note'}
    response = test_client.post("/create_note", json=body)

    assert response.status_code == 200
    data = response.json()
    assert 'id' in data
    assert "test_note" in data


def test_create_note_failure(test_client):
    body = {}
    response = test_client.post("/create_note", json=body)
    assert response.status_code == 442

"""

"""


def test_create_user():
    response = client.post(
        "/users/",
        json={"email": "deadpool@example.com", "password": "chimichangas4life"},
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["email"] == "deadpool@example.com"
    assert "id" in data
    user_id = data["id"]

    response = client.get(f"/users/{user_id}")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["email"] == "deadpool@example.com"
    assert data["id"] == user_id
"""
