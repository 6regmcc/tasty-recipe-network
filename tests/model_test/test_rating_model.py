import pytest

from sqlalchemy import inspect, Integer, DateTime


from tasty_recipe_network.db.db_connection import engine
from tasty_recipe_network.models.rating_models import Rating


@pytest.fixture(scope="function")
def db_inspector(db_session):
    return inspect(engine)


def test_db(db_inspector):
    db = db_inspector
    print(db)
    assert True


def test_model_structure_table_exists(db_inspector):
    assert db_inspector.has_table(Rating.__tablename__)


def test_db_columns(db_inspector):
    columns = {columns["name"]: columns for columns in db_inspector.get_columns("rating")}
    assert "rating_id" in columns
    assert "rating" in columns
    assert "date_created" in columns
    assert "date_modified" in columns
    assert "user_id" in columns
    assert "recipe_id" in columns
    assert len(columns) == 6


def test_column_type(db_inspector):
    columns = {columns["name"]: columns for columns in db_inspector.get_columns("rating")}
    assert isinstance(columns["rating_id"]["type"], Integer)
    assert isinstance(columns["rating"]["type"], Integer)
    assert isinstance(columns["date_created"]["type"], DateTime)
    assert isinstance(columns["date_modified"]["type"], DateTime)
    assert isinstance(columns["user_id"]["type"], Integer)
    assert isinstance(columns["recipe_id"]["type"], Integer)


def test_db_constraint(db_inspector):
    ratings_constraints = {
        constraint["name"]: constraint for constraint in db_inspector.get_check_constraints("rating")
    }
    assert "rating limits" in ratings_constraints
    assert ratings_constraints["rating limits"]["sqltext"] == "rating > 0 AND rating <= 5"


def test_db_nullable(db_inspector):
    table = "rating"
    columns = db_inspector.get_columns(table)

    expected_nullable = {
        "rating_id": False,
        "rating": False,
        "date_created": False,
        "date_modified": False,
        "user_id": False,
        "recipe_id": False,
    }

    for column in columns:
        column_name = column["name"]
        assert column["nullable"] == expected_nullable.get(
            column_name
        ), f"column '{column_name}' is not nullable as expected"


def test_server_default(db_inspector):
    columns = {columns["name"]: columns for columns in db_inspector.get_columns("rating")}
    assert columns["date_created"]["default"] == "now()"
    assert columns["date_modified"]["default"] == "now()"
    # test on update


def test_db_relationship(db_inspector):
    foreign_keys = {key["name"]: key for key in db_inspector.get_foreign_keys("rating")}
    assert "rating_recipe_id_fkey" in foreign_keys
    assert "rating_user_id_fkey" in foreign_keys
    assert foreign_keys["rating_recipe_id_fkey"]["options"] == {"ondelete": "CASCADE"}
    assert foreign_keys["rating_user_id_fkey"]["options"] == {"ondelete": "CASCADE"}
