def test_first(test_client):
    response = test_client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}


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
