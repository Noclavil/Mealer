from typing import Optional

from pydantic.main import BaseModel


class Nutrition(BaseModel):
    calories: Optional[int] = 0
    fats: Optional[int] = 0
    carbs: Optional[int] = 0
    proteins: Optional[int] = 0
