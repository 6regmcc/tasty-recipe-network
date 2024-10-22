import os

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from tasty_recipe_network.db.db_connection import Base

TEST_DATABASE_URL = os.getenv("TEST_DATABASE_URL")

engine = create_engine(TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(autoflush=False, bind=engine)


def get_test_database() -> Session:
    test_db: Session = TestingSessionLocal()
    return test_db


def db_create_all():
    Base.metadata.create_all(bind=engine, checkfirst=True)


def db_drop_all():
    Base.metadata.drop_all(bind=engine)
