import os
from datetime import datetime, timedelta, timezone
from typing import Annotated

import jwt
from fastapi import APIRouter, HTTPException

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt import InvalidTokenError
from passlib.context import CryptContext
from pydantic import BaseModel
from sqlalchemy.dialects.postgresql import psycopg2
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from starlette import status

from db.db_connection import get_db
from db.db_user_auth import db_create_user
from models.user_models import User_Auth, User_Details
from schemas.user_schema import Create_User, Return_User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
router = APIRouter()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


def get_user_by_email(db: Session, email: str):
    return db.query(User_Auth).filter(User_Auth.email == email).first()


@router.post("/create_user", response_model=Return_User)
def create_user(create_user_data: Create_User,
                db: Annotated[Session, Depends(get_db)]):
    hashed_password = get_password_hash(create_user_data.password)
    create_user_data.password = hashed_password
    try:
        new_user = db_create_user(create_user_data=create_user_data, db=db)
        return new_user
    except IntegrityError as e:
        error = e
        print(e)
        raise HTTPException(status_code=400, detail=e.orig)









def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def get_user(db: Session, username: str):
    user_auth = db.query(User_Auth).filter(User_Auth.email == username).first()
    if not user_auth:
        raise HTTPException(status_code=404, detail="Category not found")

    return User_Auth_With_Pwd(**user_auth.to_dict())


def authenticate_user(db: Session, username: str, password: str):
    user_auth = get_user(db, username)
    if not user_auth:
        return False
    if not verify_password(password, user_auth.hashed_password):
        return False
    return user_auth

"""def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
"""

# async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
# user = fake_decode_token(token)
# return user


# @router.get("/me", tags=["users"] )
# async def read_users_me(current_user: Annotated[User_Auth, Depends(get_current_user)]):
# return current_user
