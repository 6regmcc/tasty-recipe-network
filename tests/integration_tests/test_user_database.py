import pytest
import sqlalchemy

from db.db_user_auth import db_get_user_by_username, db_get_user_details_by_id


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
        db_get_user_details_by_id(user_auth_id=9999999999, db=db_session)




def test_db_create_user(db_session):
    pass
# db_create_user
