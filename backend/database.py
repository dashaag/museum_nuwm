from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from core.config import settings

engine = create_engine(
    settings.DATABASE_URL,
    # connect_args={"check_same_thread": False} # Only for SQLite
    pool_pre_ping=True # Helps with connection drops
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
