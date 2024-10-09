from typing import Annotated
from fastapi import APIRouter


from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from models.user_models import User_Auth

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

router = APIRouter()


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    #user = fake_decode_token(token)
    #return user



@router.get("/users/me", tags=["users"] )
async def read_users_me(current_user: Annotated[User_Auth, Depends(get_current_user)]):
    #return current_user