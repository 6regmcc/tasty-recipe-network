from sqlalchemy.orm import Session

from models.recipe_models import Recipe, Ingredient
from schemas.recipe_schema import Create_Recipe, Return_Recipe, Create_Ingredient


def db_create_recipe(recipe_data: Create_Recipe, db: Session):
    new_recipe = Recipe({recipe_data_field for recipe_data_field in recipe_data})
    db.add(new_recipe)
    db.commit()
    db.refresh(new_recipe)
    new_ingredients = db_create_recipe_ingredients(ingredients=recipe_data.ingredients, recipe_id=new_recipe.recipe_id, db=db)
    created_recipe = Return_Recipe(**new_recipe.to_dict(), ingredients=new_ingredients)
    return


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
