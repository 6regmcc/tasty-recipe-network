import pytest
import sqlalchemy

from tasty_recipe_network.db.db_user_auth import db_get_user_by_username, db_get_user_details_by_id, db_create_user
from tasty_recipe_network.schemas.user_schema import Create_User, Return_User


# db_get_user_by_username

def test_get_user_by_username_success(create_user_fixture, db_session):
    user = create_user_fixture
    assert db_get_user_by_username(username=user["username"], db=db_session)


def test_get_user_by_username_not_found(db_session):
    username = "fake@fake.com"
    with pytest.raises(sqlalchemy.exc.NoResultFound):
        db_get_user_by_username(username=username, db=db_session)


def test_get_user_details_by_id_success(create_user_fixture, db_session):
    user = create_user_fixture
    assert db_get_user_details_by_id(user_auth_id=user["user_id"], db=db_session)


def test_get_user_details_by_id_failure(db_session):
    with pytest.raises(sqlalchemy.exc.NoResultFound):
        db_get_user_details_by_id(user_auth_id=-1, db=db_session)


def test_db_create_user(db_session):
    new_user = Create_User(
        username="tom_smith@email.com",
        password="Abc123",
        first_name="Tom",
        last_name="Smith"
    )
    new_user = db_create_user(create_user_data=new_user, db=db_session)
    assert isinstance(new_user, Return_User)


def test_db_create_user_duplicate(create_user_fixture, db_session):
    new_user = create_user_fixture
    new_duplicate_user = Create_User(
        username=new_user["username"],
        password="Password1"
    )
    with pytest.raises(sqlalchemy.exc.IntegrityError):

        db_create_user(create_user_data=new_duplicate_user, db=db_session)
