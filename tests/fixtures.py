import os

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from starlette.testclient import TestClient
from app.main import app
from db.db_connection import get_db



@pytest.fixture(scope="function")
def test_client():
    with TestClient(app) as _client:
        yield _client


from db.db_connection import Base

TEST_DATABASE_URL = os.getenv("TEST_DATABASE_URL")

engine = create_engine(TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(autoflush=False, autocommit=False, bind=engine)


def override_get_db():
    try:
        database = TestingSessionLocal()

        Base.metadata.create_all(bind=engine, checkfirst=True)
        print('this ran')
        yield database

    finally:
        database.close()
        Base.metadata.drop_all(bind=engine)
        print('this also ran')


app.dependency_overrides[get_db] = override_get_db
