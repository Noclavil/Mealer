from typing import Optional

from pydantic.main import BaseModel

from .submodels.nutrition import Nutrition


# Shared properties
class IngredientBase(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    nutrition: Optional[Nutrition] = None


# Properties to receive on Ingredient creation
class IngredientCreate(IngredientBase):
    name: str


# Properties to receive on Ingredient update
class IngredientUpdate(IngredientBase):
    pass


# Properties shared by models stored in DB
class IngredientInDBBase(IngredientBase):
    id: int
    name: str
    owner_id: int

    class Config:
        orm_mode = True


# Properties to return to client
class Ingredient(IngredientInDBBase):
    pass


# Properties properties stored in DB
class IngredientInDB(IngredientInDBBase):
    pass
