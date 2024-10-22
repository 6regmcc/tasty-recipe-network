from typing import Optional

from sqlalchemy import ForeignKey
from sqlalchemy import String

from sqlalchemy.orm import Mapped, relationship
from sqlalchemy.orm import mapped_column

from tasty_recipe_network.db.db_connection import Base, dataclass_sql


@dataclass_sql
class Recipe(Base):
    __tablename__ = "recipe"

    recipe_id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(60))
    created_by: Mapped[int] = mapped_column(ForeignKey("user_auth.user_id"))
    is_vegan: Mapped[bool] = mapped_column(default=False)
    is_vegetarian: Mapped[str] = mapped_column(default=False)
    body: Mapped[str] = mapped_column(String(2000))
    ingredients = relationship('Ingredient', backref='recipe')


@dataclass_sql
class Ingredient(Base):
    __tablename__ = "ingredients"
    ingredient_id: Mapped[int] = mapped_column(primary_key=True)
    ingredient_name: Mapped[str] = mapped_column(String(100))
    amount: Mapped[float] = mapped_column()
    notes: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    unit: Mapped[Optional[str]] = mapped_column(default=None, nullable=True)
    is_metric: Mapped[bool] = mapped_column()
    recipe_id: Mapped[int] = mapped_column(ForeignKey("recipe.recipe_id", ondelete="CASCADE"))
