from fastapi.testclient import TestClient

from app.main import app


def test_first(test_client):
    response = test_client.get('/')
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}
