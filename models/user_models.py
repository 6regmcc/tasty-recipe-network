
from typing import Optional

from sqlalchemy import ForeignKey
from sqlalchemy import String

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column


from db.db_connection import Base


class User_Auth(Base):
    __tablename__ = "user_auth"

    user_id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(40), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String(100), nullable=False)


class User_Details(Base):
    __tablename__ = "user_details"
    user_details_id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    last_name: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    verified: Mapped[bool] = mapped_column(default=False, nullable=False)
    user_auth_id: Mapped[int] = mapped_column(ForeignKey("user_auth.user_id"))


class Notes(Base):
    __tablename__ = "notes"
    id: Mapped[int] = mapped_column(primary_key=True)
    test_note: Mapped[str] = mapped_column(String(100))
    test: Mapped[str] = mapped_column(String(100))
