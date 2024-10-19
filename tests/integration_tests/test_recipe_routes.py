from db.db_recipes import db_create_recipe_with_ingredients
from schemas.recipe_schema import Return_Recipe


def test_create_recipe(test_client, create_user_fixture, authorised_user):
    body = {
        "title": "test",
        "is_vegan": True,
        "is_vegetarian": True,
        "body": "string",
        "ingredients": [
            {
                "ingredient_name": "string",
                "amount": 0,
                "unit": "string",
                "notes": "string",
                "is_metric": True
            }
        ]
    }

    headers = {
        'Authorization': f'Bearer {authorised_user["token"]}'
    }

    response = test_client.post("/recipies/create_recipe", json=body, headers=headers)
    assert response.status_code == 200
    recipe = response.json()
    assert Return_Recipe(**recipe)
    assert recipe["title"] == "test"
    assert len(recipe["ingredients"]) == 1


def test_get_users_recipies(test_client, db_session, authorised_user, recipe_one, recipe_two, recipe_three):
    user_1 = authorised_user
    recipe1 = db_create_recipe_with_ingredients(recipe_data=recipe_one, user_id=user_1["user_id"], db=db_session)
    recipe2 = db_create_recipe_with_ingredients(recipe_data=recipe_two, user_id=user_1["user_id"], db=db_session)
    recipe3 = db_create_recipe_with_ingredients(recipe_data=recipe_three, user_id=user_1["user_id"], db=db_session)

    headers = {
        'Authorization': f'Bearer {user_1["token"]}'
    }

    response = test_client.get("recipies/user_recipies", headers=headers)
    assert response.status_code == 200
    recipies = response.json()
    assert len(recipies) == 3
    for recipie in recipies:
        assert Return_Recipe(**recipie)
