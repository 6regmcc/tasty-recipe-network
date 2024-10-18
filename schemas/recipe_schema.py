from pydantic import BaseModel


class Create_Ingredient(BaseModel):
    ingredient_name: str
    amount: float
    unit: str | None = None
    notes: str | None = None
    is_metric: bool = True


class Return_Ingredient(Create_Ingredient):
    ingredient_id: int
    recipe_id: int


class Create_Recipe(BaseModel):
    title: str  # add 60 char limit
    is_vegan: bool
    is_vegetarian: bool
    body: str

    ingredients: list[Create_Ingredient]

class Update_Recipe(BaseModel):
    title: str  # add 60 char limit
    is_vegan: bool
    is_vegetarian: bool
    body: str


class Return_Recipe(Create_Recipe):
    recipe_id: int
    ingredients: list[Return_Ingredient]
    created_by: int