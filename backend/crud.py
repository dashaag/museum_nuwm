from sqlalchemy.orm import Session
from typing import List, Optional

import models
import schemas
from security import get_password_hash # For creating manager

# --- Category CRUD --- 
def get_category(db: Session, category_id: int) -> Optional[models.Category]:
    return db.query(models.Category).filter(models.Category.id == category_id).first()

def get_category_by_name(db: Session, name: str) -> Optional[models.Category]:
    return db.query(models.Category).filter(models.Category.name == name).first()

def get_categories(db: Session, skip: int = 0, limit: int = 100) -> List[models.Category]:
    return db.query(models.Category).offset(skip).limit(limit).all()

def create_category(db: Session, category: schemas.CategoryCreate) -> models.Category:
    db_category = models.Category(**category.model_dump())
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

def update_category(db: Session, category_id: int, category_update: schemas.CategoryUpdate) -> Optional[models.Category]:
    db_category = get_category(db, category_id)
    if db_category:
        update_data = category_update.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_category, key, value)
        db.commit()
        db.refresh(db_category)
    return db_category

def delete_category(db: Session, category_id: int) -> Optional[models.Category]:
    db_category = get_category(db, category_id)
    if db_category:
        # Ensure no pieces of art are linked before deleting, or handle accordingly
        # For this example, we assume this check is done at the API level or not required
        db.delete(db_category)
        db.commit()
    return db_category

# --- PieceOfArt CRUD --- 
def get_piece_of_art(db: Session, piece_of_art_id: int) -> Optional[models.PieceOfArt]:
    return db.query(models.PieceOfArt).filter(models.PieceOfArt.id == piece_of_art_id).first()

def get_pieces_of_art(db: Session, skip: int = 0, limit: int = 100, category_id: Optional[int] = None) -> List[models.PieceOfArt]:
    query = db.query(models.PieceOfArt)
    if category_id is not None:
        query = query.filter(models.PieceOfArt.category_id == category_id)
    return query.offset(skip).limit(limit).all()

def create_piece_of_art(db: Session, piece_of_art: schemas.PieceOfArtCreate) -> models.PieceOfArt:
    db_piece_of_art = models.PieceOfArt(**piece_of_art.model_dump())
    db.add(db_piece_of_art)
    db.commit()
    db.refresh(db_piece_of_art)
    return db_piece_of_art

def update_piece_of_art(db: Session, piece_of_art_id: int, piece_of_art_update: schemas.PieceOfArtUpdate) -> Optional[models.PieceOfArt]:
    db_piece_of_art = get_piece_of_art(db, piece_of_art_id)
    if db_piece_of_art:
        update_data = piece_of_art_update.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_piece_of_art, key, value)
        db.commit()
        db.refresh(db_piece_of_art)
    return db_piece_of_art

def delete_piece_of_art(db: Session, piece_of_art_id: int) -> Optional[models.PieceOfArt]:
    db_piece_of_art = get_piece_of_art(db, piece_of_art_id)
    if db_piece_of_art:
        db.delete(db_piece_of_art)
        db.commit()
    return db_piece_of_art

# --- Manager CRUD --- 
def get_manager(db: Session, manager_id: int) -> Optional[models.Manager]:
    return db.query(models.Manager).filter(models.Manager.id == manager_id).first()

def get_manager_by_email(db: Session, email: str) -> Optional[models.Manager]:
    return db.query(models.Manager).filter(models.Manager.email == email).first()

def get_managers(db: Session, skip: int = 0, limit: int = 100) -> List[models.Manager]:
    return db.query(models.Manager).offset(skip).limit(limit).all()

def create_manager(db: Session, manager: schemas.ManagerCreate) -> models.Manager:
    hashed_password = get_password_hash(manager.password)
    db_manager = models.Manager(
        email=manager.email,
        first_name=manager.first_name,
        last_name=manager.last_name,
        hashed_password=hashed_password
    )
    db.add(db_manager)
    db.commit()
    db.refresh(db_manager)
    return db_manager

# Update and Delete for Manager can be added if needed, following similar patterns.
# For this project, manager creation is primary for seeding, updates might be out of scope for initial setup.
