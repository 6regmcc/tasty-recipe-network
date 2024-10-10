import pytest
from starlette.testclient import TestClient
from app.main import app
from db.db_connection import get_db
from tests.database.db_database_connection import get_test_database, db_create_all, db_drop_all




@pytest.fixture(scope="function")
def test_client():
    with TestClient(app) as _client:
        yield _client


@pytest.fixture(scope="module")
def set_test_db():

    db_create_all()
    yield
    #db_drop_all()


def get_test_db():
    return get_test_database()

app.dependency_overrides[get_db] = get_test_db