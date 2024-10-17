import os
from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from typing import TYPE_CHECKING
from sqlalchemy.ext.declarative import declared_attr
#from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import declarative_base

DATABASE_URL = os.getenv("DEV_DATABASE_URL")

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

#https://youtrack.jetbrains.com/issue/PY-58881
if TYPE_CHECKING:
    from dataclasses import dataclass as dataclass_sql
else:
    def dataclass_sql(cls: object) -> object:
        return cls


def db_create_all():
    # Base.metadata.clear()
    #Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine, checkfirst=True)
