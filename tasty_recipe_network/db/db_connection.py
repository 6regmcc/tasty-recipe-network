import os
from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from typing import TYPE_CHECKING
# from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import declarative_base

from tasty_recipe_network.config import DEV_DATABASE_URL

DATABASE_URL = ""
environment = os.environ.get('ENVIRONMENT')

if environment == "production":
    DATABASE_URL = os.environ.get("DATABASE_URL")
else:
    DATABASE_URL = DEV_DATABASE_URL

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autoflush=False, autocommit=False, bind=engine)


def get_db() -> Generator:
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class Base(object):
    __abstract__ = True

    def to_dict(self):
        return {field.name: getattr(self, field.name) for field in self.__table__.c}


Base = declarative_base(cls=Base)

# https://youtrack.jetbrains.com/issue/PY-58881
if TYPE_CHECKING:
    pass
else:
    def dataclass_sql(cls: object) -> object:
        return cls


def db_create_all():
    # Base.metadata.clear()
    # Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine, checkfirst=True)
