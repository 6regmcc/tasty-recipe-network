from tasty_recipe_network.db.db_recipes import db_create_recipe_with_ingredients
from tasty_recipe_network.schemas.recipe_schema import Return_Recipe


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


def test_get_users_recipes(test_client, db_session, authorised_user, recipe_one, recipe_two, recipe_three):
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


def test_get_users_recipes_failure(test_client, authorised_user, db_session):
    user_1 = authorised_user
    headers = {
        'Authorization': f'Bearer {user_1["token"]}'
    }
    response = test_client.get("recipies/user_recipies", headers=headers)
    assert response.status_code == 404
    recipies = response.json()
    assert recipies["detail"] == "No recipies found"


def test_get_recipe_by_id(test_client, db_session, authorised_user, recipe_one):
    user_1 = authorised_user
    recipe_id = db_create_recipe_with_ingredients(recipe_data=recipe_one, user_id=user_1["user_id"], db=db_session).recipe_id
    response = test_client.get(f"recipies/recipe/{recipe_id}")
    recipe = response.json()
    assert response.status_code == 200
    assert Return_Recipe(**recipe)
    assert recipe_id == recipe["recipe_id"]


def test_get_recipe_by_id_failure(test_client, db_session):
    response = test_client.get(f"recipies/recipe/99999999999")
    recipie = response.json()
    assert response.status_code == 404
    assert recipie["detail"] == "No recipie found"


def test_get_all_recipies(test_client, create_user_fixture, create_user2_fixture, recipe_one, recipe_two, recipe_three,
                            db_session):
    user_1 = create_user_fixture
    user_2 = create_user2_fixture

    recipe1 = db_create_recipe_with_ingredients(recipe_data=recipe_one, user_id=user_1["user_id"], db=db_session)
    recipe2 = db_create_recipe_with_ingredients(recipe_data=recipe_two, user_id=user_1["user_id"], db=db_session)
    recipe3 = db_create_recipe_with_ingredients(recipe_data=recipe_three, user_id=user_1["user_id"], db=db_session)
    recipe4 = db_create_recipe_with_ingredients(recipe_data=recipe_one, user_id=user_2["user_id"], db=db_session)
    recipe5 = db_create_recipe_with_ingredients(recipe_data=recipe_two, user_id=user_2["user_id"], db=db_session)

    response = test_client.get("recipies/all")
    recipies = response.json()
    assert len(recipies) == 5
    recipie_ids = set()
    for recipe in recipies:
        assert Return_Recipe(**recipe)
        recipie_ids.add(recipe["recipe_id"])
    assert len(recipie_ids) == 5
    assert recipe1.recipe_id in recipie_ids
    assert recipe2.recipe_id in recipie_ids
    assert recipe3.recipe_id in recipie_ids
    assert recipe4.recipe_id in recipie_ids
    assert recipe5.recipe_id in recipie_ids


def test_update_recipe(test_client, authorised_user, recipe_one, db_session):
    user = authorised_user["user_id"]
    token = authorised_user["token"]
    headers = {
        'Authorization': f'Bearer {authorised_user["token"]}'
    }
    new_recipe = db_create_recipe_with_ingredients(recipe_data=recipe_one, user_id=user, db=db_session)
    recipe_update_data = {

            "title": "update_title",
            "is_vegan": True,
            "is_vegetarian": False,
            "body": "updated body",


    }
    response = test_client.put(f"recipies/update_recipe/{new_recipe.recipe_id}", json=recipe_update_data, headers=headers)
    updated_recipe = response.json()
    assert response.status_code == 200
    assert updated_recipe["title"] == recipe_update_data["title"]
    assert updated_recipe["is_vegan"] == recipe_update_data["is_vegan"]
    assert updated_recipe["is_vegetarian"] == recipe_update_data["is_vegetarian"]
    assert updated_recipe["body"] == recipe_update_data["body"]