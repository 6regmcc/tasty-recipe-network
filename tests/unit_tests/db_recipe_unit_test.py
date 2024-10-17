from db.db_recipes import db_create_recipe_ingredients


def test_create_recipe():
    pass


def test_create_ingredients(return_ingredients, create_recipe, db_session):
    ingredients_to_add = return_ingredients
    new_recipe = create_recipe
    added_ingredients = db_create_recipe_ingredients(ingredients=ingredients_to_add, recipe_id=new_recipe["recipe_id"], db=db_session)
    assert added_ingredients
