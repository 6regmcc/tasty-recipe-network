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
from db.db_user_auth import db_create_user, db_get_user_by_username
from models.user_models import User_Auth, User_Details
from schemas.user_schema import Create_User, Return_User, Return_User_With_Pwd, Authenticate_User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="user/token")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
router = APIRouter()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 300


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


def authenticate_user(username: str, password: str, db: Session):
    user = db_get_user_by_username(username=username, db=db)
    print(user)
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user


@router.post("/create_user", response_model=Return_User)
def create_user(create_user_data: Create_User,
                db: Annotated[Session, Depends(get_db)]):
    hashed_password = get_password_hash(create_user_data.password)
    create_user_data.password = hashed_password
    try:
        new_user = db_create_user(create_user_data=create_user_data, db=db)
        return new_user
    except IntegrityError as e:
        raise HTTPException(status_code=400, detail=e.orig.args)


@router.post("/token")
async def login(
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Annotated[Session, Depends(get_db)]
) -> Token:
    user = authenticate_user(username=form_data.username, password=form_data.password, db=db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def get_user(db: Session, username: str):
    user_auth = db.query(User_Auth).filter(User_Auth.email == username).first()
    if not user_auth:
        raise HTTPException(status_code=404, detail="User not found")

    return Return_User_With_Pwd(**user_auth.to_dict())


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
# user = fake_decode_token(token)
# return user


# @router.get("/me", tags=["users"] )
# async def read_users_me(current_user: Annotated[User_Auth, Depends(get_current_user)]):
# return current_user


def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], db: Session):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except InvalidTokenError:
        raise credentials_exception
    user = db_get_user_by_username(username=token_data.username, db=db)
    if user is None:
        raise credentials_exception
    return user


@router.get("/me", response_model=Return_User)
async def read_users_me(token: Annotated[str, Depends(oauth2_scheme)], db: Annotated[Session, Depends(get_db)]):
    user = get_current_user(token=token, db=db)
    return user
