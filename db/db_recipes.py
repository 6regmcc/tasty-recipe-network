from typing import Sequence

import sqlalchemy
from sqlalchemy import select
from sqlalchemy.orm import Session

from models.recipe_models import Recipe, Ingredient
from schemas.recipe_schema import Create_Recipe, Return_Recipe, Create_Ingredient, Return_Ingredient, Update_Recipe


def db_get_recipe(recipe_id: int, db: Session) -> Recipe:
    found_recipe = db.get(Recipe, recipe_id)
    if not found_recipe:
        raise sqlalchemy.exc.NoResultFound
    return found_recipe


def db_get_ingredient(ingredient_id: int, db: Session) -> Ingredient:
    found_ingredient = db.get(Ingredient, ingredient_id)
    if not found_ingredient:
        raise sqlalchemy.exc.NoResultFound
    return found_ingredient


def db_get_ingredients(recipe_id: int, db: Session) -> Sequence[Ingredient]:
    found_ingredients: Sequence[Ingredient] = db.scalars(
        select(Ingredient).where(Ingredient.recipe_id == recipe_id)).all()
    if not found_ingredients:
        raise sqlalchemy.exc.NoResultFound
    return found_ingredients


def db_get_recipe_with_ingredients(recipe_id: int, db: Session) -> Return_Recipe:
    recipe = db.scalars(select(Recipe).where(Recipe.recipe_id == recipe_id)).one()
    return_recipe = Return_Recipe(**recipe.to_dict(),
                                  ingredients=[ingredient.to_dict() for ingredient in recipe.ingredients])
    return return_recipe


def db_get_recipe_id_from_ingredient_id(ingredient_id: int, db: Session) -> int:
    found_ingredient = db.query(Ingredient).filter(Ingredient.ingredient_id == ingredient_id).one()
    return found_ingredient.recipe_id


def db_edit_recipe(recipe: Update_Recipe, recipe_id: int, db: Session):
    recipe_to_update = db.get(Recipe, recipe_id)
    if not recipe_to_update:
        raise sqlalchemy.exc.NoResultFound
    for key, value in recipe:
        setattr(recipe_to_update, key, value)
    db.commit()
    ingredients = db_get_ingredients(recipe_id=recipe_id, db=db)
    return Return_Recipe(**recipe_to_update.to_dict(), ingredients=[Return_Ingredient(**ingredient.to_dict()) for ingredient in ingredients])


def db_edit_ingredient(ingredient: Create_Ingredient, ingredient_id: int, db: Session) -> Ingredient:
    ingredient_to_update = db.get(Ingredient, ingredient_id)
    if not ingredient_to_update:
        raise sqlalchemy.exc.NoResultFound

    for key, value in ingredient:
        setattr(ingredient_to_update, key, value)
    db.commit()
    return ingredient_to_update


def add_ingredient_to_recipe(new_ingredient: Create_Ingredient, recipe_id: int, db: Session) -> Ingredient:
    ingredient_to_add = Ingredient(**new_ingredient.model_dump(), recipe_id=recipe_id)
    try:
        db.add(ingredient_to_add)
    except sqlalchemy.exc.IntegrityError as e:
        raise e

    db.commit()
    db.refresh(ingredient_to_add)
    return ingredient_to_add


def delete_ingredient(ingredient_id: int, db: Session):
    ingredient_to_delete = db.query(Ingredient).filter(Ingredient.ingredient_id == ingredient_id).delete()
    db.commit()
    return ingredient_to_delete


def delete_recipe(recipe_id: int, db: Session):
    recipe_to_delete = db.query(Recipe).filter(Recipe.recipe_id == recipe_id).delete()

    db.commit()
    return recipe_to_delete


def db_create_recipe(recipe_data: Create_Recipe, user_id: int, db: Session):
    new_recipe = Recipe(**recipe_data.model_dump(exclude={"ingredients"}), created_by=user_id)
    db.add(new_recipe)
    db.commit()
    db.refresh(new_recipe)
    return new_recipe


def db_create_recipe_ingredients(ingredients: list[Create_Ingredient], recipe_id: int, db: Session):
    add_ingredients = []
    for ingredient in ingredients:
        new_ingredient = Ingredient(**ingredient.model_dump(), recipe_id=recipe_id)
        add_ingredients.append(new_ingredient)
    db.add_all(add_ingredients)
    db.commit()
    for mapped_ingredient in add_ingredients:
        db.refresh(mapped_ingredient)
    return add_ingredients


def db_create_recipe_with_ingredients(recipe_data: Create_Recipe, user_id: int, db: Session):
    new_recipe = None
    new_ingredients = None
    try:
        new_recipe = db_create_recipe(recipe_data=recipe_data, user_id=user_id, db=db)
    except Exception as e:
        raise e

    try:
        new_ingredients = db_create_recipe_ingredients(ingredients=recipe_data.ingredients,
                                                       recipe_id=new_recipe.recipe_id, db=db)
    except Exception as e:
        db.delete(new_recipe)
        db.commit()
        raise e
    created_recipe = Return_Recipe(**new_recipe.to_dict(),
                                   ingredients=[Return_Ingredient(**ingredient.to_dict()) for ingredient in
                                                new_ingredients])
    return created_recipe


def db_get_users_recipies(user_id: int, db: Session):
    found_recipies = db.scalars(select(Recipe).where(Recipe.created_by == user_id)).all()
    return_recipies = [
        Return_Recipe(**recipe.to_dict(), ingredients=[ingredient.to_dict() for ingredient in recipe.ingredients]) for
        recipe in found_recipies]

    return return_recipies


def db_get_all_recipies(db: Session) -> list[Return_Recipe]:
    found_recipies = db.scalars(select(Recipe)).all()
    return_recipies = [
        Return_Recipe(**recipe.to_dict(), ingredients=[ingredient.to_dict() for ingredient in recipe.ingredients]) for
        recipe in found_recipies]

    return return_recipies


def db_check_if_user_owns_recipe(recipe_id: int, user_id: int, db: Session):
    recipe = db.scalars(select(Recipe).filter(Recipe.created_by == user_id and Recipe.recipe_id == recipe_id)).first()
    if not recipe:
        raise sqlalchemy.exc.NoResultFound
    return True

