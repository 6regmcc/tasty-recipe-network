from typing import Annotated

import sqlalchemy
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette.requests import Request

from authentication.user_auth_routes import oauth2_scheme, router, get_current_user
from db.db_connection import get_db
from db.db_recipes import db_create_recipe_with_ingredients, db_get_users_recipies, db_get_recipe_with_ingredients, \
    db_get_all_recipies
from schemas.recipe_schema import Create_Recipe

recipe_router = APIRouter(
    prefix="/recipies",
    tags=["Recipies"],
    dependencies=[Depends(oauth2_scheme)]
)

recipe_router_no_auth = APIRouter(
    prefix="/recipies",
    tags=["Recipies"],

)


@recipe_router_no_auth.get("/recipe/{id}")
def get_recipe_by_id(id: int, db: Annotated[Session, Depends(get_db)]):
    try:
        return db_get_recipe_with_ingredients(recipe_id=id, db=db)
    except sqlalchemy.exc.NoResultFound:
        raise HTTPException(status_code=404, detail="No recipie found")


@recipe_router_no_auth.get("/all")
def get_all_recipies(db: Annotated[Session, Depends(get_db)]):
    return db_get_all_recipies(db=db)


@recipe_router.get("/user_recipies")
def get_users_recipies(db: Annotated[Session, Depends(get_db)], token: Annotated[str, Depends(oauth2_scheme)]):
    user_id = get_current_user(token=token, db=db).user_id
    users_recipies = db_get_users_recipies(user_id=user_id, db=db)
    if not users_recipies:
        raise HTTPException(status_code=404, detail="No recipies found")
    return users_recipies


@recipe_router.post("/create_recipe")
def create_recipe(recipe_data: Create_Recipe, db: Annotated[Session, Depends(get_db)],
                  token: Annotated[str, Depends(oauth2_scheme)]):
    user_id = get_current_user(token=token, db=db).user_id
    try:
        new_recipe = db_create_recipe_with_ingredients(recipe_data=recipe_data, user_id=user_id, db=db)
    except Exception as e:
        raise e
    return new_recipe


@recipe_router.put("/update_recipe/{id}")
def update_recipe():
    pass
