import os
from dotenv import load_dotenv
from pathlib import Path
from typing import List, Union

# Determine the path to the .env file. Assumes .env is in the `backend` directory.
# If running from within `backend` directory, Path.cwd() is `backend`
# If docker-compose runs it, WORKDIR is /app which is mapped to backend
# For local scripts (like alembic env.py trying to load .env), ensure correct path resolution.
# The most robust way is to ensure .env is in the same dir as this config.py or one level up (project root)
# For this project, .env is in the `backend` directory, same as this config.py (when WORKDIR=/app).

env_path = Path(__file__).resolve().parent.parent / '.env' # Points to backend/.env
if env_path.exists():
    load_dotenv(dotenv_path=env_path)
else:
    # Fallback for cases where .env might be in current working directory (e.g. local script run from backend/)
    load_dotenv(dotenv_path=Path('.') / '.env')

class Settings:
    PROJECT_NAME: str = "Museum API"
    PROJECT_VERSION: str = "1.0.0"

    POSTGRES_USER: str = os.getenv("POSTGRES_USER", "museum_user")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD", "museum_password")
    POSTGRES_SERVER: str = os.getenv("POSTGRES_SERVER", "db") # 'db' is the service name in docker-compose
    POSTGRES_PORT: str = os.getenv("POSTGRES_PORT", "5432")
    POSTGRES_DB: str = os.getenv("POSTGRES_DB", "museum_db")
    
    # DATABASE_URL is constructed to ensure it uses the potentially overridden individual components
    _db_url_env = os.getenv("DATABASE_URL")
    if _db_url_env:
        DATABASE_URL: str = _db_url_env
    else:
        DATABASE_URL: str = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}"

    SECRET_KEY: str = os.getenv("SECRET_KEY", "a_very_secret_key_please_change_it_in_env")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

    # For initial data seeding
    INIT_DB: bool = os.getenv("INIT_DB", "False").lower() in ('true', '1', 't', 'yes')
    ADMIN_EMAIL: str = os.getenv("ADMIN_EMAIL", "admin@museum.com")
    ADMIN_PASSWORD: str = os.getenv("ADMIN_PASSWORD", "Admin123!")

    # CORS - expecting a comma-separated string from env or defaults to a list
    _cors_origins_env = os.getenv("BACKEND_CORS_ORIGINS")
    if _cors_origins_env:
        BACKEND_CORS_ORIGINS: List[str] = [origin.strip() for origin in _cors_origins_env.split(',')]
    else:
        BACKEND_CORS_ORIGINS: List[str] = [
            "http://localhost:5173", # Default Vite dev server
            "http://127.0.0.1:5173",
            "http://localhost:3000", # Common React dev server port
            "http://localhost",      # For docker access sometimes
            # Add other origins as needed, e.g., your production frontend URL
        ]

settings = Settings()

# # You can add a small test print here for debugging .env loading if needed
# print(f"--- Settings Initialized ---")
# print(f"DATABASE_URL: {settings.DATABASE_URL}")
# print(f"SECRET_KEY: {'*' * len(settings.SECRET_KEY) if settings.SECRET_KEY else 'Not Set'}")
# print(f"INIT_DB: {settings.INIT_DB} (Type: {type(settings.INIT_DB)})")
# print(f"ADMIN_EMAIL: {settings.ADMIN_EMAIL}")
# print(f"CORS Origins: {settings.BACKEND_CORS_ORIGINS}")
# print(f"--- End Settings --- ")
