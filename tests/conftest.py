import os

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from starlette.testclient import TestClient

from app.main import app
from authentication.user_auth_routes import get_password_hash
from db.db_connection import Base, get_db
from models.user_models import User_Auth, User_Details
from schemas.user_schema import Return_User

TEST_DATABASE_URL = os.getenv("TEST_DATABASE_URL")

engine = create_engine(TEST_DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create tables in the database
Base.metadata.create_all(bind=engine)


# Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def db_session():
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    yield session
    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture(scope="function")
def test_client(db_session):
    def override_get_db():
        try:
            yield db_session
        finally:
            db_session.close()

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture(scope="function")
def create_user_fixture(db_session):
    new_user = User_Auth(
        username="tom4@gmail.com",
        password=get_password_hash("Password1"),

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

    return {**new_user.to_dict(), **new_user_details.to_dict()}
