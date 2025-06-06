from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

import crud
import models
import schemas
from api import deps # For get_current_manager and get_db
from database import get_db # Direct import for get_db

router = APIRouter()

@router.get("/", response_model=List[schemas.Category])
def read_categories(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    # current_manager: models.Manager = Depends(deps.get_current_manager) # Uncomment if auth needed for listing
):
    """
    Retrieve all categories.
    Publicly accessible.
    """
    categories = crud.get_categories(db, skip=skip, limit=limit)
    return categories

@router.get("/{category_id}", response_model=schemas.Category)
def read_category(
    category_id: int,
    db: Session = Depends(get_db),
    # current_manager: models.Manager = Depends(deps.get_current_manager) # Uncomment if auth needed
):
    """
    Retrieve a specific category by ID.
    Publicly accessible.
    """
    db_category = crud.get_category(db, category_id=category_id)
    if db_category is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
    return db_category

# POST, PUT, DELETE for categories are not explicitly required by the task for managers.
# If they were, they would look similar to PieceOfArt endpoints, guarded by get_current_manager.

# Example: Create Category (Manager Only) - if it were required
@router.post("/", response_model=schemas.Category, status_code=status.HTTP_201_CREATED)
def create_category(
    *, # Ensures all following parameters are keyword-only
    db: Session = Depends(get_db),
    category_in: schemas.CategoryCreate,
    current_manager: models.Manager = Depends(deps.get_current_manager)
):
    """
    Create new category. (Manager only)
    """
    existing_category = crud.get_category_by_name(db, name=category_in.name)
    if existing_category:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A category with this name already exists."
        )
    category = crud.create_category(db=db, category=category_in)
    return category


@router.put("/{category_id}", response_model=schemas.Category)
def update_category(
    *,
    db: Session = Depends(get_db),
    category_id: int,
    category_in: schemas.CategoryUpdate,
    current_manager: models.Manager = Depends(deps.get_current_manager)
):
    """
    Update a category. (Manager only)
    """
    db_category = crud.get_category(db, category_id=category_id)
    if not db_category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
    # Check for name conflict if name is being changed
    if category_in.name and category_in.name != db_category.name:
        existing_category_with_new_name = crud.get_category_by_name(db, name=category_in.name)
        if existing_category_with_new_name and existing_category_with_new_name.id != category_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Another category with this name already exists."
            )
    category = crud.update_category(db=db, category_id=category_id, category_update=category_in)
    return category


@router.delete("/{category_id}", response_model=schemas.Category)
def delete_category(
    *,
    db: Session = Depends(get_db),
    category_id: int,
    current_manager: models.Manager = Depends(deps.get_current_manager)
):
    """
    Delete a category. (Manager only)
    """
    db_category = crud.get_category(db, category_id=category_id)
    if not db_category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
    # Add any pre-delete checks here, e.g., if category is in use by pieces of art
    # For now, directly delete.
    deleted_category = crud.delete_category(db=db, category_id=category_id)
    return deleted_category
