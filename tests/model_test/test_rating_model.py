import pytest
from sqlalchemy import inspect


@pytest.fixture(scope="function")
def db_inspector(db_session):
    return inspect(db_session().bind)


def test_db(db_inspector):
    db = db_inspector
    print(db)
    assert True
