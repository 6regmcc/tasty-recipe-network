from unittest.mock import Mock

import pytest
import sqlalchemy

from db.db_recipes import db_create_recipe_ingredients, db_create_recipe, db_create_recipe_with_ingredients, \
    delete_recipe, delete_ingredient, get_recipe_id_from_ingredient_id, get_ingredients
from models.recipe_models import Recipe, Ingredient
from schemas.recipe_schema import Create_Recipe, Return_Recipe


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


def test_create_recipe_with_ingredients(recipe_one, db_session):
    new_recipe = db_create_recipe_with_ingredients(recipe_data=recipe_one, db=db_session)
    assert new_recipe
    assert isinstance(new_recipe, Return_Recipe)


def test_create_recipe_with_ingredients_exception(recipe_one, db_session, mocker):
    mock_db_delete = Mock()
    sqlalchemy.orm.Session.delete = mock_db_delete
    mocker.patch("db.db_recipes.db_create_recipe_ingredients", side_effect=ValueError('Test exception handling'))

    with pytest.raises(ValueError):
        new_recipe = db_create_recipe_with_ingredients(recipe_data=recipe_one, db=db_session)
        assert new_recipe is False
        mock_db_delete.assert_called()


def test_delete_recipe(create_recipe_with_ingredients, db_session):
    recipe_to_delete = create_recipe_with_ingredients
    example_recipe_id = recipe_to_delete.recipe_id
    example_ingredient_id = recipe_to_delete.ingredients[0].ingredient_id
    assert db_session.query(Recipe).filter(Recipe.recipe_id == example_recipe_id).one()
    assert db_session.query(Ingredient).filter(Ingredient.ingredient_id == example_ingredient_id).one()
    deleted_recipe = delete_recipe(recipe_id=recipe_to_delete.recipe_id, db=db_session)
    found_recipe = db_session.query(Recipe).filter(Recipe.recipe_id == example_recipe_id).first()
    assert found_recipe is None
    found_ingredient = db_session.query(Ingredient).filter(Ingredient.ingredient_id == example_ingredient_id).first()
    assert found_ingredient is None


def test_delete_ingredient(create_recipe_with_ingredients, db_session):
    new_recipe = create_recipe_with_ingredients
    example_ingredient_id = new_recipe.ingredients[0].ingredient_id
    assert db_session.query(Ingredient).filter(Ingredient.ingredient_id == example_ingredient_id)
    delete_ingredient(example_ingredient_id, db_session)

    with pytest.raises(sqlalchemy.exc.NoResultFound):
        db_session.query(Ingredient).filter(Ingredient.ingredient_id == example_ingredient_id).one()


def test_get_recipe_id_from_ingredient_id_success(create_recipe_with_ingredients, db_session):
    new_recipe = create_recipe_with_ingredients
    example_ingredient_id = new_recipe.ingredients[0].ingredient_id
    found_recipie_id = get_recipe_id_from_ingredient_id(ingredient_id=example_ingredient_id, db=db_session)

    assert found_recipie_id == new_recipe.recipe_id


def test_get_recipe_id_from_ingredient_id_failure(db_session):
    example_ingredient_id = 1
    with pytest.raises(sqlalchemy.exc.NoResultFound):
        get_recipe_id_from_ingredient_id(ingredient_id=example_ingredient_id, db=db_session)


def test_get_ingredients(create_recipe_with_ingredients, db_session):
    recipe_id = create_recipe_with_ingredients.recipe_id
    found_ingredients = get_ingredients(recipe_id, db_session)
    for ingredient in found_ingredients:
        assert ingredient.recipe_id == recipe_id


def test_get_ingredients_failure(db_session):
    recipe_id = 999999999999999999
    with pytest.raises(sqlalchemy.exc.NoResultFound):
        found_ingredients = get_ingredients(recipe_id, db_session)

