from typing import List, Any

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

import crud
import models
import schemas
from api import deps
from database import get_db # Direct import for get_db

router = APIRouter()

@router.get("/", response_model=List[schemas.PieceOfArt])
def read_pieces_of_art(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    category_id: int = None, # Optional filter by category_id
) -> Any:
    """
    Retrieve all pieces of art. Publicly accessible.
    Can be filtered by category_id.
    """
    pieces = crud.get_pieces_of_art(db, skip=skip, limit=limit, category_id=category_id)
    return pieces

@router.post("/", response_model=schemas.PieceOfArt, status_code=status.HTTP_201_CREATED)
def create_piece_of_art(
    *, # Ensures all following parameters are keyword-only
    db: Session = Depends(get_db),
    piece_in: schemas.PieceOfArtCreate,
    current_manager: models.Manager = Depends(deps.get_current_manager)
) -> Any:
    """
    Create new piece of art. (Manager only)
    """
    # Check if category exists
    category = crud.get_category(db, category_id=piece_in.category_id)
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Category with id {piece_in.category_id} not found."
        )
    piece = crud.create_piece_of_art(db=db, piece_of_art=piece_in)
    return piece

@router.get("/{piece_id}", response_model=schemas.PieceOfArt)
def read_piece_of_art(
    piece_id: int,
    db: Session = Depends(get_db),
) -> Any:
    """
    Get a specific piece of art by ID. Publicly accessible.
    """
    db_piece = crud.get_piece_of_art(db, piece_of_art_id=piece_id)
    if db_piece is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Piece of art not found")
    return db_piece

@router.put("/{piece_id}", response_model=schemas.PieceOfArt)
def update_piece_of_art(
    *, # Ensures all following parameters are keyword-only
    db: Session = Depends(get_db),
    piece_id: int,
    piece_in: schemas.PieceOfArtUpdate,
    current_manager: models.Manager = Depends(deps.get_current_manager)
) -> Any:
    """
    Update a piece of art. (Manager only)
    """
    db_piece = crud.get_piece_of_art(db, piece_of_art_id=piece_id)
    if not db_piece:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Piece of art not found")
    
    # If category_id is being updated, check if the new category exists
    if piece_in.category_id is not None:
        category = crud.get_category(db, category_id=piece_in.category_id)
        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Category with id {piece_in.category_id} not found for update."
            )
            
    piece = crud.update_piece_of_art(db=db, piece_of_art_id=piece_id, piece_of_art_update=piece_in)
    return piece

@router.delete("/{piece_id}", response_model=schemas.PieceOfArt)
def delete_piece_of_art(
    *, # Ensures all following parameters are keyword-only
    db: Session = Depends(get_db),
    piece_id: int,
    current_manager: models.Manager = Depends(deps.get_current_manager)
) -> Any:
    """
    Delete a piece of art. (Manager only)
    """
    db_piece = crud.get_piece_of_art(db, piece_of_art_id=piece_id)
    if not db_piece:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Piece of art not found")
    
    deleted_piece = crud.delete_piece_of_art(db=db, piece_of_art_id=piece_id)
    # The crud function already returns the deleted object or None
    # We've already confirmed it exists, so it should return the object
    return deleted_piece
