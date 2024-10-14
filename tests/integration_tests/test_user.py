from models.user_models import User_Auth, User_Details


def test_create_user(test_client):
    body = {
        "username": "tom@email.com",
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


def test_create_existing_user(test_client):
    body = {
        "username": "tom1@email.com",
        "password": "Password1",
        "first_name": "Tom",
        "last_name": "Smith"
    }

    response = test_client.post("/user/create_user", json=body)
    response2 = test_client.post("/user/create_user", json=body)
    assert response2.status_code == 400
    data = response2.json()
    assert data["detail"] == "Username already exists"


def test_create_user_required_fields(test_client):
    body = {

        "password": "Password1",
        "first_name": "Tom",
        "last_name": "Smith"
    }
    response = test_client.post("/user/create_user", json=body)
    assert response.status_code == 422
    body = {

        "username": "tom2@email.com",
        "first_name": "Tom",
        "last_name": "Smith"
    }
    response2 = test_client.post("/user/create_user", json=body)
    assert response2.status_code == 422


def test_create_user_optional_fields(test_client):
    body = {
        "username": "tom3@email.com",
        "password": "Password1"

    }
    response = test_client.post("/user/create_user", json=body)
    assert response.status_code == 200

    data = response.json()
    assert "user_id" in data
    assert data["username"] == "tom3@email.com"
    assert "password" not in data
    assert data["first_name"] is None
    assert data["last_name"] is None


def test_login_success(test_client, db_session):
    new_user = User_Auth(
        username="tom4@gmail.com",
        password="Password1",

    )
    db_session.add(new_user)
    db_session.commit()
    db_session.refresh(new_user)
    new_user_details = User_Details(
        first_name="Tom",
        last_name="Smith",
        user_auth_id=new_user.user_id
    )
    db_session.add(new_user_details)
    db_session.commit()
    db_session.refresh(new_user_details)
    assert "user_id" in new_user.to_dict()
    assert "user_details_id" in new_user_details.to_dict()
    assert "user_auth_id" in new_user_details.to_dict()




def test_incorrect_username_password(test_client):
    pass
