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
        'Authorization': f'Bearer {authorised_user}'
    }

    response = test_client.post("/recipies/create_recipe", json=body, headers=headers)
    assert response.status_code == 200
    data = response.json()
