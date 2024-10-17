import os

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from starlette.testclient import TestClient

from app.main import app
from authentication.user_auth_routes import get_password_hash
from db.db_connection import Base, get_db
from models.recipe_models import Recipe
from models.user_models import User_Auth, User_Details
from schemas.recipe_schema import Create_Ingredient
from schemas.user_schema import Return_User

TEST_DATABASE_URL = os.getenv("TEST_DATABASE_URL")

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
    ingredients_to_add: list[Create_Ingredient] = []
    for ingredient in ingredients:
        ingredients_to_add.append(Create_Ingredient(**ingredient))
    return ingredients_to_add



