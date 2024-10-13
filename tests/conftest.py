import pytest

from app.main import app
from db.db_connection import get_db
from .database.db_database_connection import db_create_all, db_drop_all, get_test_database
from .fixtures import test_client


# test
# db_create_all()
db_drop_all()






