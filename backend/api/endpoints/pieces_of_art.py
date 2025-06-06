from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

import crud
import models
import schemas
from api import deps # For get_db and potentially get_current_manager later

router = APIRouter()

@router.get("/", response_model=List[schemas.PieceOfArt])
def read_pieces_of_art(
    db: Session = Depends(deps.get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=200),
    category_id: Optional[int] = Query(None)
):
    """
    Retrieve all pieces of art.
    Optionally filter by category_id.
    Supports pagination with skip and limit.
    """
    pieces_of_art = crud.get_pieces_of_art(db, skip=skip, limit=limit, category_id=category_id)
    return pieces_of_art

# We can add POST, PUT, DELETE later as needed for full admin CRUD
