from datetime import datetime


from sqlalchemy import CheckConstraint, ForeignKey, DateTime, func
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from tasty_recipe_network.db.db_connection import Base


class Rating(Base):
    __tablename__ = "rating"
    rating_id: Mapped[int] = mapped_column(primary_key=True, auto_increment=True)
    rating: Mapped[int] = mapped_column(CheckConstraint("rating > 0 AND rating <=5 ", name="rating limits"))
    date_created: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    date_modified: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), onupdate=func.now(), server_default=func.now()
    )
    user_id: Mapped[int] = mapped_column(ForeignKey("user_auth.user_id", ondelete="CASCADE"))
    recipe_id: Mapped[int] = mapped_column(ForeignKey("recipe.recipe_id", ondelete="CASCADE"))
    # add unique recipe and user id constraint
