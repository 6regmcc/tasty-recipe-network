from typing import Annotated

import sqlalchemy
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from tasty_recipe_network.routes.user_auth_routes import oauth2_scheme, get_current_user
from tasty_recipe_network.db.db_connection import get_db
from tasty_recipe_network.db.db_recipes import db_create_recipe_with_ingredients, db_get_users_recipies, db_get_recipe_with_ingredients, \
    db_get_all_recipies, db_check_if_user_owns_recipe, db_edit_recipe
from tasty_recipe_network.schemas.recipe_schema import Create_Recipe, Update_Recipe, Return_Recipe

recipe_router = APIRouter(
    prefix="/recipies",
    tags=["Recipies"],
    dependencies=[Depends(oauth2_scheme)]
)

recipe_router_no_auth = APIRouter(
    prefix="/recipies",
    tags=["Recipies"],

)


@recipe_router_no_auth.get("/recipe/{id}", response_model=Return_Recipe)
def get_recipe_by_id(id: int, db: Annotated[Session, Depends(get_db)]):
    try:
        return db_get_recipe_with_ingredients(recipe_id=id, db=db)
    except sqlalchemy.exc.NoResultFound:
        raise HTTPException(status_code=404, detail="No recipie found")


@recipe_router_no_auth.get("/all", response_model=list[Return_Recipe])
def get_all_recipies(db: Annotated[Session, Depends(get_db)]):
    return db_get_all_recipies(db=db)


@recipe_router.get("/user_recipies", response_model=list[Return_Recipe])
def get_users_recipies(db: Annotated[Session, Depends(get_db)], token: Annotated[str, Depends(oauth2_scheme)]):
    user_id = get_current_user(token=token, db=db).user_id
    users_recipies = db_get_users_recipies(user_id=user_id, db=db)
    if not users_recipies:
        raise HTTPException(status_code=404, detail="No recipies found")
    return users_recipies


@recipe_router.post("/create_recipe", response_model=Return_Recipe)
def create_recipe(recipe_data: Create_Recipe, db: Annotated[Session, Depends(get_db)],
                  token: Annotated[str, Depends(oauth2_scheme)]):
    user_id = get_current_user(token=token, db=db).user_id
    try:
        new_recipe = db_create_recipe_with_ingredients(recipe_data=recipe_data, user_id=user_id, db=db)
    except Exception as e:
        raise e
    return new_recipe


@recipe_router.put("/update_recipe/{recipe_id}", response_model=Return_Recipe)
def update_recipe(recipe_id: int, recipe_data: Update_Recipe, db: Annotated[Session, Depends(get_db)], token: Annotated[str, Depends(oauth2_scheme)]):
    user_id = get_current_user(token=token, db=db).user_id

    try:
        db_check_if_user_owns_recipe(recipe_id=recipe_id, user_id=user_id, db=db)
    except sqlalchemy.exc.NoResultFound:
        raise HTTPException(status_code=404, detail="No recipie found")
    try:
        return db_edit_recipe(recipe=recipe_data, recipe_id=recipe_id, db=db)
    except Exception as e:
        if e.args[0]:
            raise HTTPException(status_code=500, detail=f"{e.args[0]}")
        else:
            raise HTTPException(status_code=500, detail=f"Server Error")

