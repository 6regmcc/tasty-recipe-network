from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette.requests import Request

from authentication.user_auth_routes import oauth2_scheme, router, get_current_user
from db.db_connection import get_db
from schemas.recipe_schema import Create_Recipe

recipe_router = APIRouter(
    prefix="/recipies",
    tags=["Recipies"],
    dependencies = [Depends(oauth2_scheme)]
)


@recipe_router.post("/create_recipe")
def create_recipe(new_recipe: Create_Recipe, db: Annotated[Session, Depends(get_db)], token: Annotated[str, Depends(oauth2_scheme)]):
    user_id = get_current_user(token=token, db=db).user_id

    return token


@recipe_router.get("/test")
def test_stuff(db: Annotated[Session, Depends(get_db)], token: Annotated[str, Depends(oauth2_scheme)]):

    return user_id