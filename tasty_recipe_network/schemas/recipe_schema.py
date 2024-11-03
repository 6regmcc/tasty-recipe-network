from pydantic import BaseModel


class CreateIngredient(BaseModel):
    ingredient_name: str
    amount: float
    unit: str | None = None
    notes: str | None = None
    is_metric: bool = True


class ReturnIngredient(CreateIngredient):
    ingredient_id: int
    recipe_id: int


class CreateRecipe(BaseModel):
    title: str  # add 60 char limit
    is_vegan: bool
    is_vegetarian: bool
    body: str
    ingredients: list[CreateIngredient]

class ReturnRecipe(BaseModel):
    title: str  # add 60 char limit
    is_vegan: bool
    is_vegetarian: bool
    body: str
    recipe_id: int
    ingredients: list[ReturnIngredient]
    created_by: int

class UpdateRecipe(BaseModel):
    title: str  # add 60 char limit
    is_vegan: bool
    is_vegetarian: bool
    body: str


