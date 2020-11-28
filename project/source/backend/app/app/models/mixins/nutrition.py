from sqlalchemy import Column, Integer


class NutritionMixin:
    calories = Column(Integer)
    fats = Column(Integer)
    carbs = Column(Integer)
    proteins = Column(Integer)
