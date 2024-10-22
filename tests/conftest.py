import os

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from starlette.testclient import TestClient

from tasty_recipe_network.main import app
from tasty_recipe_network.routes.user_auth_routes import get_password_hash
from tasty_recipe_network.db.db_connection import Base, get_db
from tasty_recipe_network.models.recipe_models import Recipe
from tasty_recipe_network.models.user_models import User_Auth, User_Details
from tasty_recipe_network.schemas.recipe_schema import Create_Ingredient, Create_Recipe
from tasty_recipe_network.db.db_recipes import db_create_recipe_with_ingredients

TEST_DATABASE_URL = os.getenv("TEST_DATABASE_URL")
ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")
engine = create_engine(TEST_DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create tables in the database
Base.metadata.create_all(bind=engine)


# Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def db_session():
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    yield session
    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture(scope="function")
def test_client(db_session):
    def override_get_db():
        try:
            yield db_session
        finally:
            db_session.close()

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture(scope="function")
def create_user_fixture(db_session):
    new_user = User_Auth(
        username="tom4@gmail.com",
        password=get_password_hash("Password1"),

    )
    db_session.add(new_user)
    db_session.commit()
    db_session.refresh(new_user)
    new_user_details = User_Details(
        first_name="Tom",
        last_name="Smith",
        user_auth_id=new_user.user_id
    )
    db_session.add(new_user_details)
    db_session.commit()
    db_session.refresh(new_user_details)

    return {**new_user.to_dict(), **new_user_details.to_dict()}


@pytest.fixture(scope="function")
def authorised_user(create_user_fixture, test_client):
    new_user = create_user_fixture
    body = {
        "username": new_user["username"],
        "password": 'Password1'

    }
    response = test_client.post("user/token", data=body)
    data = response.json()

    token = data["access_token"]
    user_data = {
        "user_id": new_user["user_id"],
        "token": token
    }
    return user_data


@pytest.fixture(scope="function")
def create_recipe(db_session, create_user_fixture):
    new_user = create_user_fixture
    new_recipe = Recipe(
        title="Giant Lazy Meatballs",
        created_by=new_user["user_id"],
        is_vegan=False,
        is_vegetarian=False,
        body="""
Crumble bread into a bowl and mix in milk thoroughly using a fork. Let stand for 10 to 15 minutes.

Combine beef and pork in a large bowl and mix well using 2 forks. Add salt, black pepper, oregano, onion powder, garlic powder, cayenne, olive oil, Parmesan, parsley, eggs, and the breadcrumb mixture. Mix using 2 forks until everything is evenly combined. Wrap and chill in the refrigerator for 1 hour.

Preheat the oven to 400 degrees F (200 degrees C). Lightly grease a roasting pan or baking dish. Using damp hands, roll 4 giant meatballs, and place in the prepared pan.

Bake in the preheated oven until an instant read thermometer inserted near the center of meatballs reads 160 to 165 degrees F (71 to 74 degrees C), 40 to 45 minutes.

Remove meatballs from the oven, and spoon tomato sauce evenly over meatballs. Sprinkle first with Monterey Jack cheese, and then with Parmigiano-Reggiano.

Return meatballs to the oven, and bake until sauce is hot and cheese is melted, 5 to 10 minutes more. Top with parsley and serve.""")

    db_session.add(new_recipe)
    db_session.commit()
    db_session.refresh(new_recipe)
    return_recipe = {**new_recipe.to_dict()}
    return return_recipe


@pytest.fixture(scope="function")
def create_recipe_with_ingredients(recipe_one, create_user_fixture, db_session):
    new_recipe = recipe_one
    user_id = create_user_fixture["user_id"]
    created_recipe = db_create_recipe_with_ingredients(recipe_data=new_recipe, user_id=user_id, db=db_session)
    return created_recipe


@pytest.fixture(scope="function")
def return_ingredients(create_recipe):
    ingredients = [
        {
            "amount": 4,
            "ingredient_name": "large slices stale white bread",
            "notes": "crusts removed",
            "is_metric": False,

        },
        {
            "amount": 0.5,
            "unit": "cups",
            "ingredient_name": "milk",
            "is_metric": False,

        },
        {
            "amount": 1,
            "unit": "lb",
            "ingredient_name": "ground beef",
            "is_metric": False,

        },
        {
            "amount": 1,
            "unit": "lb",
            "ingredient_name": "ground pork",
            "is_metric": False,

        },
        {
            "amount": 2.5,
            "unit": "teaspoon",
            "ingredient_name": "kosher salt",
            "is_metric": False,

        },
        {
            "amount": 1,
            "unit": "teaspoon",
            "ingredient_name": "black pepper",
            "notes": "freshly ground",
            "is_metric": False,

        },
        {
            "amount": 0.25,
            "unit": "teaspoon",
            "ingredient_name": "dried oregano",
            "is_metric": False,

        },
        {
            "amount": 1,
            "unit": "teaspoon",
            "ingredient_name": " onion powder",
            "is_metric": False,

        },
        {
            "amount": 1,
            "unit": "teaspoon",
            "ingredient_name": "garlic powder",
            "is_metric": False,

        },
        {
            "amount": 1,
            "unit": "pinch",
            "ingredient_name": "cayenne pepper",
            "is_metric": False,

        },
        {
            "amount": 1,
            "unit": "tablespoon",
            "ingredient_name": "olive oil",
            "is_metric": False,

        },
        {
            "amount": 0.25,
            "unit": "cup",
            "ingredient_name": "Parmigiano-Reggiano",
            "notes": "freshly grated",
            "is_metric": False,

        },
        {
            "amount": 0.333,
            "unit": "cup",
            "ingredient_name": "Italian parsley",
            "notes": "chopped fresh (optional)",
            "is_metric": False,

        },
        {
            "amount": 1,
            "ingredient_name": "Italian parsley",
            "notes": "chopped fresh (optional)",
            "is_metric": False,

        },
        {
            "amount": 2,
            "ingredient_name": "large eggs",
            "notes": "lightly beaten",
            "is_metric": False,

        }

    ]
    ingredients_to_add: list[Create_Ingredient] = [Create_Ingredient(**ingredient) for ingredient in ingredients]

    return ingredients_to_add


@pytest.fixture(scope="function")
def recipe_one():
    ingredients = [
        {
            "amount": 2,
            "unit": "teaspoon",
            "ingredient_name": "kosher salt",
            "notes": "plus more to taste",
            "is_metric": False,

        },
        {
            "amount": 0.5,
            "unit": "teaspoon",
            "ingredient_name": "black pepper",
            "notes": "freshly ground",
            "is_metric": False,

        },
        {
            "amount": 1,
            "unit": "teaspoon",
            "ingredient_name": "black pepper",
            "notes": "freshly ground",
            "is_metric": False,

        },
        {
            "amount": 6,

            "ingredient_name": "large chicken thighs",
            "notes": "bone-in, skin-on",
            "is_metric": False,

        },
        {
            "amount": 1,
            "unit": "teaspoon",
            "ingredient_name": "black pepper",
            "notes": "freshly ground",
            "is_metric": False,

        },
        {
            "amount": 1,
            "unit": "tablespoon",
            "ingredient_name": "vegetable oil",

            "is_metric": False,

        },
        {
            "amount": 0.5,
            "unit": "cup",
            "ingredient_name": "shallots",
            "notes": "diced",
            "is_metric": False,

        },
        {
            "amount": 3,

            "ingredient_name": "garlic cloves",
            "notes": "sliced",
            "is_metric": False,

        },
        {
            "amount": 1,
            "unit": "tablespoon",
            "ingredient_name": "tomato paste",

            "is_metric": False,

        },
        {
            "amount": 0.5,
            "unit": "cup",
            "ingredient_name": "wine vinegar",

            "is_metric": False,

        },
        {
            "amount": 1,
            "unit": "cup",
            "ingredient_name": "dry white wine",

            "is_metric": False,

        },
        {
            "amount": 1,
            "unit": "cup",
            "ingredient_name": "chicken broth",

            "is_metric": False,

        },
        {
            "amount": 0.25,
            "unit": "cup",
            "ingredient_name": "heavy cream",
            "notes": "freshly ground",
            "is_metric": False,

        },
        {
            "amount": 1,
            "unit": "tablespoon",
            "ingredient_name": "butter",
            "notes": "cold unsalted",
            "is_metric": False,

        },
        {
            "amount": 1,
            "unit": "tablespoon",
            "ingredient_name": "fresh tarragon",
            "notes": "freshly chopped",
            "is_metric": False,

        }
    ]
    ingredients_to_add = [Create_Ingredient(**ingredient) for ingredient in ingredients]

    new_recipe = Create_Recipe(
        title="Poulet au Vinaigre (Chicken with Vinegar)",
        is_vegan=False,
        is_vegetarian=False,
        ingredients=ingredients_to_add,
        body="""

Preheat the oven to 325 degrees F (165 degrees C).

Mix salt and black pepper together, and season chicken first on the meat side. Turn chicken skin side up, pat dry, and season with the rest of the mixture.

Heat oil in an ovenproof pan over high heat. Place thighs in, skin side down, and sear until well browned, without disturbing, about 5 minutes. Turn and sear meat side for 2 minutes. Remove to plate and turn off heat.

Drain or use a paper towel to remove excess fat in the pan, leaving 1 to 2 tablespoons.

Turn heat to medium, add shallots and a pinch of salt, and sauté for a few minutes, just until shallots turn translucent. Add garlic and tomato paste and cook, stirring, for another minute.

Add vinegar and cook, stirring and scraping up browned bits from the bottom of the pan. Add wine and broth, raise heat to high, and bring to a simmer. Add chicken back in, skin side up, and turn off heat. 

Bake in the preheated oven until meat is fork tender, 40 to 45 minutes. An instant read thermometer inserted near the center should read about 195 degrees F (90 degrees C).

Remove thighs from pan, and turn heat to high. Boil for a few minutes, or until volume is reduced by half. Add cream and cook until sauce starts to thicken slightly, a few minutes more. 

Reduce heat to low and add butter and tarragon. Stir until butter disappears. Add chicken back to the pan, and baste with sauce for a few minutes before serving. """
    )
    return new_recipe


@pytest.fixture(scope="function")
def recipe_two():
    recipe = {
        "title": "recipe_2",
        "is_vegan": True,
        "is_vegetarian": True,
        "body": "string",

    }

    ingredients = [
        {
            "ingredient_name": "recipe_2a",
            "amount": 0,
            "unit": "string",
            "notes": "string",
            "is_metric": True
        },
        {
            "ingredient_name": "recipe_2b",
            "amount": 0,
            "unit": "string",
            "notes": "string",
            "is_metric": False
        }
    ]

    ingredients_to_add = [Create_Ingredient(**ingredient) for ingredient in ingredients]
    recipe_to_add = Create_Recipe(**recipe, ingredients=ingredients_to_add)
    return recipe_to_add


@pytest.fixture(scope="function")
def recipe_three():
    recipe = {
        "title": "recipe_three",
        "is_vegan": True,
        "is_vegetarian": False,
        "body": "string",

    }
    ingredients = [
        {
            "ingredient_name": "recipe_three_a",
            "amount": 0,
            "unit": "string",
            "notes": "string",
            "is_metric": False
        },
        {
            "ingredient_name": "recipe_three_b",
            "amount": 0,
            "unit": "string",
            "notes": "string",
            "is_metric": False
        }
    ]
    ingredients_to_add = [Create_Ingredient(**ingredient) for ingredient in ingredients]
    recipe_to_add = Create_Recipe(**recipe, ingredients=ingredients_to_add)
    return recipe_to_add


@pytest.fixture(scope="function")
def create_user2_fixture(db_session):
    new_user = User_Auth(
        username="tom5@gmail.com",
        password=get_password_hash("Password1"),

    )
    db_session.add(new_user)
    db_session.commit()
    db_session.refresh(new_user)
    new_user_details = User_Details(
        first_name="Tom",
        last_name="Smith",
        user_auth_id=new_user.user_id
    )
    db_session.add(new_user_details)
    db_session.commit()
    db_session.refresh(new_user_details)

    return {**new_user.to_dict(), **new_user_details.to_dict()}


