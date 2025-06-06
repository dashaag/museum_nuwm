import logging
from sqlalchemy.orm import Session

from database import SessionLocal, engine, Base
from models import Category, PieceOfArt, Manager # Ensure all models are imported for Base.metadata.create_all
import crud
import schemas
from core.config import settings
from security import get_password_hash

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Sample Data
CATEGORIES_DATA = ["Art", "Sculpture", "Painting", "Photography"]

PIECES_OF_ART_DATA = [
    {"name": "Sunset Overdrive", "description": "A vibrant depiction of a sunset.", "category_name": "Painting", "image_url": "https://picsum.photos/seed/sunset/600/400"},
    {"name": "The Thinker's Shadow", "description": "A modern take on a classic pose.", "category_name": "Sculpture", "image_url": "https://picsum.photos/seed/thinker/600/400"},
    {"name": "Abstract Flow", "description": "Colors and shapes in harmony.", "category_name": "Art", "image_url": "https://picsum.photos/seed/abstract/600/400"},
    {"name": "Urban Solitude", "description": "A lone figure in a bustling city.", "category_name": "Photography", "image_url": "https://picsum.photos/seed/urban/600/400"},
    {"name": "Nature's Embrace", "description": "A serene forest landscape.", "category_name": "Painting", "image_url": "https://picsum.photos/seed/nature/600/400"},
    {"name": "Bronze Dreams", "description": "An intricate bronze statue.", "category_name": "Sculpture", "image_url": "https://picsum.photos/seed/bronze/600/400"},
    {"name": "Digital Canvas", "description": "Exploring the boundaries of digital art.", "category_name": "Art", "image_url": "https://picsum.photos/seed/digital/600/400"},
    {"name": "Monochrome Moods", "description": "Black and white cityscapes.", "category_name": "Photography", "image_url": "https://picsum.photos/seed/monochrome/600/400"},
    {"name": "Ocean's Whisper", "description": "The calming sound of waves captured.", "category_name": "Painting", "image_url": "https://picsum.photos/seed/ocean/600/400"},
    {"name": "Steel Symphony", "description": "A large outdoor metal installation.", "category_name": "Sculpture", "image_url": "https://picsum.photos/seed/steel/600/400"},
    {"name": "Pixelated Visions", "description": "Art created from individual pixels.", "category_name": "Art", "image_url": "https://picsum.photos/seed/pixel/600/400"},
    {"name": "Portraits of Life", "description": "Candid shots of everyday people.", "category_name": "Photography", "image_url": "https://picsum.photos/seed/portraits/600/400"},
    {"name": "Celestial Dance", "description": "Nebulae and galaxies on canvas.", "category_name": "Painting", "image_url": "https://picsum.photos/seed/celestial/600/400"},
    {"name": "Ephemeral Forms", "description": "Sculptures made from light and shadow.", "category_name": "Sculpture", "image_url": "https://picsum.photos/seed/ephemeral/600/400"},
    {"name": "Glitch Aesthetics", "description": "The beauty in digital errors.", "category_name": "Art", "image_url": "https://picsum.photos/seed/glitch/600/400"},
    {"name": "Silent Witness", "description": "Ancient trees in black and white.", "category_name": "Photography", "image_url": "https://picsum.photos/seed/trees/600/400"}
]

MANAGER_DATA = {
    "first_name": "Admin",
    "last_name": "User",
    "email": settings.ADMIN_EMAIL,
    "password": settings.ADMIN_PASSWORD
}

def init_db(db: Session) -> None:
    # This function assumes Alembic has already created the tables.
    # It's for populating data.

    # Create Categories
    created_categories = {}
    for cat_name in CATEGORIES_DATA:
        category = crud.get_category_by_name(db, name=cat_name)
        if not category:
            category_in = schemas.CategoryCreate(name=cat_name)
            category = crud.create_category(db, category=category_in)
            logger.info(f"Created category: {category.name}")
        created_categories[cat_name] = category

    # Create Pieces of Art
    for art_data in PIECES_OF_ART_DATA:
        # Check if piece already exists by name (simple check, could be more robust)
        # For this seeding, we'll assume if a piece with the same name and category exists, we skip.
        category = created_categories.get(art_data["category_name"])
        if not category:
            logger.warning(f"Category {art_data['category_name']} not found for art piece {art_data['name']}. Skipping.")
            continue
        
        # A more robust check would be to query for the piece of art by name AND category_id
        # existing_piece = db.query(PieceOfArt).filter_by(name=art_data["name"], category_id=category.id).first()
        # if existing_piece:
        #     logger.info(f"Art piece '{art_data['name']}' in category '{category.name}' already exists. Skipping.")
        #     continue

        art_in = schemas.PieceOfArtCreate(
            name=art_data["name"],
            description=art_data["description"],
            image_url=art_data["image_url"],
            category_id=category.id
        )
        # Simple check: if any piece with this name exists, skip (to avoid duplicates on re-run if names are unique constraint)
        # This is not ideal if names are not unique across categories. A better check is above.
        # For now, let's assume we want to avoid re-creating if any piece with this name exists.
        # This part needs careful consideration based on actual uniqueness constraints.
        # For simplicity of seeding, we'll try to create and let DB constraints handle if any.
        # However, it's better to check first to avoid partial commits or errors during seeding.
        
        # Let's refine the check: query for piece by name AND category_id to be more specific
        existing_art_piece = db.query(PieceOfArt).filter(
            PieceOfArt.name == art_data["name"],
            PieceOfArt.category_id == category.id
        ).first()

        if not existing_art_piece:
            crud.create_piece_of_art(db, piece_of_art=art_in)
            logger.info(f"Created art piece: {art_in.name} in category {category.name}")
        else:
            logger.info(f"Art piece '{art_data['name']}' in category '{category.name}' already exists. Skipping.")

    # Create Manager User
    manager = crud.get_manager_by_email(db, email=MANAGER_DATA["email"])
    if not manager:
        manager_in = schemas.ManagerCreate(
            first_name=MANAGER_DATA["first_name"],
            last_name=MANAGER_DATA["last_name"],
            email=MANAGER_DATA["email"],
            password=MANAGER_DATA["password"]
        )
        crud.create_manager(db, manager=manager_in)
        logger.info(f"Created manager user: {manager_in.email}")
    else:
        logger.info(f"Manager user {MANAGER_DATA['email']} already exists. Skipping.")

def main():
    logger.info("Starting database initialization/seeding...")
    db = SessionLocal()
    try:
        # Optional: Create tables if they don't exist (e.g., for a very first run without Alembic)
        # This is generally handled by Alembic in the entrypoint.sh, so might be redundant or even conflicting.
        # If Alembic is the source of truth for schema, this line should be removed or commented out.
        # Base.metadata.create_all(bind=engine) 
        # logger.info("Tables checked/created (if Base.metadata.create_all was run).")

        if settings.INIT_DB:
            logger.info("INIT_DB is true. Proceeding with data seeding.")
            init_db(db)
            logger.info("Data seeding process completed.")
        else:
            logger.info("INIT_DB is false. Skipping data seeding.")
            
    except Exception as e:
        logger.error(f"Error during DB initialization: {e}", exc_info=True)
    finally:
        db.close()
    logger.info("Database initialization/seeding script finished.")

if __name__ == "__main__":
    # This check ensures that if this script is imported, main() is not run automatically.
    # It will only run if the script is executed directly (e.g., python initial_data.py).
    # The entrypoint.sh script will call `python initial_data.py` directly.
    main()
