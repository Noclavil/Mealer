from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api import deps
from app import crud, models, schemas

router = APIRouter()


@router.get("/", response_model=List[schemas.Ingredient])
def read_ingredients(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve ingredients.
    """
    if crud.user.is_superuser(current_user):
        ingredients = crud.ingredient.get_multi(db, skip=skip, limit=limit)
    else:
        ingredients = crud.ingredient.get_multi_by_owner(
            db=db, owner_id=current_user.id, skip=skip, limit=limit
        )
    return ingredients


@router.post("/", response_model=schemas.Ingredient)
def create_ingredient(
    *,
    db: Session = Depends(deps.get_db),
    ingredient_in: schemas.IngredientCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new ingredient.
    """
    ingredient = crud.ingredient.create_with_owner(
        db=db, obj_in=ingredient_in, owner_id=current_user.id
    )
    return ingredient


@router.put("/{id}", response_model=schemas.Ingredient)
def update_ingredient(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    ingredient_in: schemas.IngredientUpdate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update an ingredient.
    """
    ingredient = crud.ingredient.get(db=db, id=id)
    if not ingredient:
        raise HTTPException(status_code=404, detail="Ingredient not found")
    if not crud.user.is_superuser(current_user) and (
        ingredient.owner_id != current_user.id
    ):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    ingredient = crud.ingredient.update(db=db, db_obj=ingredient, obj_in=ingredient_in)
    return ingredient


@router.get("/{id}", response_model=schemas.Ingredient)
def read_ingredient(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get ingredient by ID.
    """
    ingredient = crud.ingredient.get(db=db, id=id)
    if not ingredient:
        raise HTTPException(status_code=404, detail="Ingredient not found")
    if not crud.user.is_superuser(current_user) and (
        ingredient.owner_id != current_user.id
    ):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    return ingredient


@router.delete("/{id}", response_model=schemas.Ingredient)
def delete_ingredient(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete an ingredient.
    """
    ingredient = crud.ingredient.get(db=db, id=id)
    if not ingredient:
        raise HTTPException(status_code=404, detail="Ingredient not found")
    if not crud.user.is_superuser(current_user) and (
        ingredient.owner_id != current_user.id
    ):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    ingredient = crud.ingredient.remove(db=db, id=id)
    return ingredient
