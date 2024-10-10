import os
from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.ext.declarative import declarative_base

from db.db_connection import Base

TEST_DATABASE_URL = os.getenv("TEST_DATABASE_URL")

engine = create_engine(TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(autoflush=False, autocommit=False, bind=engine)


def get_test_database() -> Session:
    test_db: Session = TestingSessionLocal()
    return test_db


def db_create_all():
    Base.metadata.create_all(bind=engine, checkfirst=True)


def db_drop_all():
    Base.metadata.drop_all(bind=engine)
