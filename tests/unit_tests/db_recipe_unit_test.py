from unittest.mock import Mock

import pytest
import sqlalchemy

from db.db_recipes import db_create_recipe_ingredients, db_create_recipe, db_create_recipe_with_ingredients, \
    delete_recipe, delete_ingredient, db_get_ingredients, db_get_recipe, \
    db_get_ingredient, db_get_recipe_with_ingredients, add_ingredient_to_recipe, db_edit_ingredient, \
    db_get_recipe_id_from_ingredient_id, db_edit_recipe, db_get_all_recipies, \
    db_get_users_recipies
from models.recipe_models import Recipe, Ingredient
from schemas.recipe_schema import Create_Recipe, Return_Recipe, Create_Ingredient, Update_Recipe


def test_create_ingredients(return_ingredients, create_recipe, db_session):
    ingredients_to_add = return_ingredients
    new_recipe = create_recipe
    added_ingredients = db_create_recipe_ingredients(ingredients=ingredients_to_add, recipe_id=new_recipe["recipe_id"],
                                                     db=db_session)
    assert added_ingredients
    assert isinstance(added_ingredients, list)
    assert isinstance(added_ingredients[0], Ingredient)


def test_create_recipe(recipe_one, create_user_fixture, db_session):
    new_recipe = recipe_one
    user_id = create_user_fixture["user_id"]
    new_recipe = db_create_recipe(new_recipe, user_id, db_session)
    assert new_recipe
    assert isinstance(new_recipe, Recipe)


def test_create_recipe_with_ingredients(recipe_one, create_user_fixture, db_session):
    new_recipe = recipe_one
    user_id = create_user_fixture["user_id"]
    created_recipe = db_create_recipe_with_ingredients(recipe_data=new_recipe, user_id=user_id, db=db_session)
    assert created_recipe
    assert isinstance(created_recipe, Return_Recipe)


def test_create_recipe_with_ingredients_exception(recipe_one, create_user_fixture, db_session, mocker):
    new_recipe = recipe_one
    user_id = create_user_fixture["user_id"]
    mock_db_delete = Mock()
    sqlalchemy.orm.Session.delete = mock_db_delete
    mocker.patch("db.db_recipes.db_create_recipe_ingredients", side_effect=ValueError('Test exception handling'))

    with pytest.raises(ValueError):
        new_recipe = db_create_recipe_with_ingredients(recipe_data=new_recipe, user_id=user_id, db=db_session)
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
    found_recipie_id = db_get_recipe_id_from_ingredient_id(ingredient_id=example_ingredient_id, db=db_session)

    assert found_recipie_id == new_recipe.recipe_id


def test_get_recipe_id_from_ingredient_id_failure(db_session):
    example_ingredient_id = 1
    with pytest.raises(sqlalchemy.exc.NoResultFound):
        db_get_recipe_id_from_ingredient_id(ingredient_id=example_ingredient_id, db=db_session)


def test_get_ingredients(create_recipe_with_ingredients, db_session):
    recipe_id = create_recipe_with_ingredients.recipe_id
    found_ingredients = db_get_ingredients(recipe_id, db_session)
    for ingredient in found_ingredients:
        assert ingredient.recipe_id == recipe_id


def test_get_ingredients_failure(db_session):
    recipe_id = 999999999999999999
    with pytest.raises(sqlalchemy.exc.NoResultFound):
        found_ingredients = db_get_ingredients(recipe_id, db_session)


def test_get_recipe(create_recipe_with_ingredients, db_session):
    recipe_id = create_recipe_with_ingredients.recipe_id
    found_recipe = db_get_recipe(recipe_id=recipe_id, db=db_session)
    assert found_recipe.recipe_id == recipe_id
    assert isinstance(found_recipe, Recipe)


def test_get_recipe_failure(db_session):
    recipe_id = 999999999999999999
    with pytest.raises(sqlalchemy.exc.NoResultFound):
        found_recipe = db_get_recipe(recipe_id=recipe_id, db=db_session)


def test_get_ingredient(create_recipe_with_ingredients, db_session):
    ingredient_id = create_recipe_with_ingredients.ingredients[0].ingredient_id
    found_ingredient = db_get_ingredient(ingredient_id=ingredient_id, db=db_session)
    assert isinstance(found_ingredient, Ingredient)


def test_get_ingredient_not_found(db_session):
    ingredient_id = 9999999999999
    with pytest.raises(sqlalchemy.exc.NoResultFound):
        found_ingredient = db_get_ingredient(ingredient_id=ingredient_id, db=db_session)


def test_get_recipe_with_ingredients(create_recipe_with_ingredients, db_session):
    new_recipe = create_recipe_with_ingredients
    recipe_id = new_recipe.recipe_id
    found_recipe = db_get_recipe_with_ingredients(recipe_id=recipe_id, db=db_session)
    assert isinstance(found_recipe, Return_Recipe)
    assert found_recipe.recipe_id == recipe_id
    assert len(found_recipe.ingredients) == len(new_recipe.ingredients)


def test_get_recipe_with_ingredients_not_found(db_session):
    recipe_id = 9999999999
    with pytest.raises(sqlalchemy.exc.NoResultFound):
        found_recipe = db_get_recipe_with_ingredients(recipe_id=recipe_id, db=db_session)


def test_add_ingredient_to_recipe(create_recipe_with_ingredients, db_session):
    recipe_id = create_recipe_with_ingredients.recipe_id
    new_ingredient = Create_Ingredient(
        amount=1,
        unit="teaspoon",
        ingredient_name="paprika",
        is_metric=False,
    )

    added_ingredient = add_ingredient_to_recipe(new_ingredient=new_ingredient, recipe_id=recipe_id, db=db_session)
    assert added_ingredient.recipe_id == recipe_id
    assert isinstance(added_ingredient, Ingredient)


def test_add_ingredient_to_recipe_failure(db_session):
    recipe_id = 999999999
    new_ingredient = Create_Ingredient(
        amount=1,
        unit="teaspoon",
        ingredient_name="paprika",
        is_metric=False,
    )
    with pytest.raises(sqlalchemy.exc.IntegrityError):
        added_ingredient = add_ingredient_to_recipe(new_ingredient=new_ingredient, recipe_id=recipe_id, db=db_session)


def test_edit_ingredient(create_recipe_with_ingredients, db_session):
    ingredient_to_update = create_recipe_with_ingredients
    ingredient_id = ingredient_to_update.ingredients[0].ingredient_id
    ingredient_update_data = Create_Ingredient(
        amount=999,
        unit="lb",
        ingredient_name="paprika",
        is_metric=True,
    )
    updated_ingredient = db_edit_ingredient(ingredient=ingredient_update_data, ingredient_id=ingredient_id,
                                            db=db_session)
    assert isinstance(updated_ingredient, Ingredient)
    assert updated_ingredient.ingredient_id == ingredient_id
    assert updated_ingredient.amount == ingredient_update_data.amount
    assert updated_ingredient.unit == ingredient_update_data.unit
    assert updated_ingredient.ingredient_name == ingredient_update_data.ingredient_name
    assert updated_ingredient.is_metric == ingredient_update_data.is_metric


def test_edit_ingredient_failure(db_session):
    ingredient_id = 999999999999
    ingredient_update_data = Create_Ingredient(
        amount=999,
        unit="lb",
        ingredient_name="paprika",
        is_metric=True,
    )

    with pytest.raises(sqlalchemy.exc.NoResultFound):
        updated_ingredient = db_edit_ingredient(ingredient=ingredient_update_data, ingredient_id=ingredient_id,
                                                db=db_session)


def test_db_edit_recipe(create_recipe_with_ingredients, db_session):
    recipe_to_update = create_recipe_with_ingredients
    recipe_id = recipe_to_update.recipe_id
    update_recipe_data = Update_Recipe(
        title="Updated title",
        is_vegan=True,
        is_vegetarian=True,
        body="Updated Body"
    )

    updated_recipe = db_edit_recipe(update_recipe_data, recipe_id, db_session)
    assert isinstance(updated_recipe, Recipe)
    assert updated_recipe.recipe_id == recipe_id
    assert updated_recipe.title == update_recipe_data.title
    assert updated_recipe.is_vegan == update_recipe_data.is_vegan
    assert update_recipe_data.is_vegetarian == update_recipe_data.is_vegetarian
    assert update_recipe_data.body == update_recipe_data.body


def test_db_edit_recipe_failure(db_session):
    recipe_id = -1
    update_recipe_data = Update_Recipe(
        title="Updated title",
        is_vegan=True,
        is_vegetarian=True,
        body="Updated Body"
    )
    with pytest.raises(sqlalchemy.exc.NoResultFound):
        updated_recipe = db_edit_recipe(update_recipe_data, recipe_id, db_session)






def test_get_all_recipies(create_user_fixture, create_user2_fixture, recipe_one, recipe_two, recipe_three, db_session):
    user_1 = create_user_fixture
    user_2 = create_user2_fixture

    recipe1 = db_create_recipe_with_ingredients(recipe_data=recipe_one, user_id=user_1["user_id"], db=db_session)
    recipe2 = db_create_recipe_with_ingredients(recipe_data=recipe_two, user_id=user_1["user_id"], db=db_session)
    recipe3 = db_create_recipe_with_ingredients(recipe_data=recipe_three, user_id=user_1["user_id"], db=db_session)
    recipe4 = db_create_recipe_with_ingredients(recipe_data=recipe_one, user_id=user_2["user_id"], db=db_session)
    recipe5 = db_create_recipe_with_ingredients(recipe_data=recipe_two, user_id=user_2["user_id"], db=db_session)

    recipes = db_get_all_recipies(db=db_session)
    assert len(recipes) == 5
    assert len(recipes[3].ingredients) == 15
    assert recipes[0].created_by == user_1["user_id"]
    assert recipes[3].created_by == user_2["user_id"]
    for recipe in recipes:
        assert isinstance(recipe, Return_Recipe)


def test_get_users_recipies(create_user_fixture, create_user2_fixture, recipe_one, recipe_two, recipe_three,
                            db_session):
    user_1 = create_user_fixture
    user_2 = create_user2_fixture

    recipe1 = db_create_recipe_with_ingredients(recipe_data=recipe_one, user_id=user_1["user_id"], db=db_session)
    recipe2 = db_create_recipe_with_ingredients(recipe_data=recipe_two, user_id=user_1["user_id"], db=db_session)
    recipe3 = db_create_recipe_with_ingredients(recipe_data=recipe_three, user_id=user_1["user_id"], db=db_session)
    recipe4 = db_create_recipe_with_ingredients(recipe_data=recipe_one, user_id=user_2["user_id"], db=db_session)
    recipe5 = db_create_recipe_with_ingredients(recipe_data=recipe_two, user_id=user_2["user_id"], db=db_session)

    user_1_recipies = db_get_users_recipies(user_id=user_1["user_id"], db=db_session)
    user_2_recipies = db_get_users_recipies(user_id=user_2["user_id"], db=db_session)
    assert len(user_1_recipies) == 3
    assert len(user_2_recipies) == 2
    for recipe in user_1_recipies:
        assert isinstance(recipe, Return_Recipe)

    for recipe in user_2_recipies:
        assert isinstance(recipe, Return_Recipe)