from db.db_recipes import db_create_recipe_ingredients, db_create_recipe
from models.recipe_models import Recipe, Ingredient
from schemas.recipe_schema import Create_Recipe


def test_create_ingredients(return_ingredients, create_recipe, db_session):
    ingredients_to_add = return_ingredients
    new_recipe = create_recipe
    added_ingredients = db_create_recipe_ingredients(ingredients=ingredients_to_add, recipe_id=new_recipe["recipe_id"],
                                                     db=db_session)
    assert added_ingredients
    assert isinstance(added_ingredients, list)
    assert isinstance(added_ingredients[0], Ingredient)


def test_create_recipe(recipe_one, db_session):

    new_recipe = db_create_recipe(recipe_one, db_session)
    assert new_recipe
    assert isinstance(new_recipe, Recipe)

