from typing import TYPE_CHECKING

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.db.base_class import Base

from .mixins import NutritionMixin

if TYPE_CHECKING:
    from .user import User  # noqa: F401


class Ingredient(NutritionMixin, Base):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    categroy = Column(String, index=True)
    owner_id = Column(Integer, ForeignKey("user.id"), nullable=True)
    owner = relationship("User", back_populates="ingredients")
