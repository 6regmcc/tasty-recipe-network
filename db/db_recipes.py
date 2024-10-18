from typing import Sequence

import sqlalchemy
from sqlalchemy import select
from sqlalchemy.orm import Session

from models.recipe_models import Recipe, Ingredient
from schemas.recipe_schema import Create_Recipe, Return_Recipe, Create_Ingredient, Return_Ingredient


def get_recipe(recipe_id: int, db: Session) -> Recipe:
    found_recipe = db.query(Recipe).filter(Recipe.recipe_id == recipe_id).one()
    return found_recipe


def get_ingredient(ingredient_id: int, db: Session) -> Ingredient:
    found_ingredient = db.query(Ingredient).filter(Ingredient.ingredient_id == ingredient_id).one()
    return found_ingredient


def get_ingredients(recipe_id: int, db: Session) -> Sequence[Ingredient]:
    found_ingredients: Sequence[Ingredient] = db.scalars(select(Ingredient).where(Ingredient.recipe_id == recipe_id)).all()
    if not found_ingredients:
        raise sqlalchemy.exc.NoResultFound
    return found_ingredients


def get_recipe_with_ingredients():
    pass


def get_recipe_id_from_ingredient_id(ingredient_id: int, db: Session) -> int:
    found_ingredient = db.query(Ingredient).filter(Ingredient.ingredient_id == ingredient_id).one()
    return found_ingredient.recipe_id


def db_edit_recipe():
    pass


def db_edit_ingredient():
    pass


def add_ingredient_to_recipe():
    pass


def delete_ingredient(ingredient_id: int, db: Session):
    ingredient_to_delete = db.query(Ingredient).filter(Ingredient.ingredient_id == ingredient_id).delete()
    db.commit()
    return ingredient_to_delete


def delete_recipe(recipe_id: int, db: Session):
    recipe_to_delete = db.query(Recipe).filter(Recipe.recipe_id == recipe_id).delete()

    db.commit()
    return recipe_to_delete


def db_create_recipe(recipe_data: Create_Recipe, db: Session):
    new_recipe = Recipe(**recipe_data.model_dump(exclude={"ingredients"}))
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


def db_create_recipe_with_ingredients(recipe_data: Create_Recipe, db: Session):
    new_recipe = None
    new_ingredients = None
    try:
        new_recipe = db_create_recipe(recipe_data=recipe_data, db=db)
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
