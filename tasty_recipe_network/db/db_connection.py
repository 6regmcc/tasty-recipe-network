import os
from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker, DeclarativeBase
from typing import TYPE_CHECKING
# from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import declarative_base

from tasty_recipe_network.config import DEV_DATABASE_URL


def get_environment() -> str:
    environment =  os.environ.get('ENVIRONMENT')
    if environment is None:
        raise ValueError("ENVIRONMENT environment variable not set")
    else:
        return environment


def get_db_url() -> str:
    db_url = os.environ.get("DATABASE_URL")
    if db_url is None:
        raise ValueError("DATABASE_URL environment variable not set")
    else:
        return db_url

CURR_DATABASE_URL = get_db_url() if get_environment() == "production" else DEV_DATABASE_URL


engine = create_engine(CURR_DATABASE_URL)
SessionLocal = sessionmaker(autoflush=False, autocommit=False, bind=engine)


def get_db() -> Generator:
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()



class Base(DeclarativeBase):
    def to_dict(self):
        return {field.name: getattr(self, field.name) for field in self.__table__.c}




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
