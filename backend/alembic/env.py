import os
from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Import your models' Base metadata object for 'autogenerate' support
# This requires your models.py to be importable and define Base
# Ensure that the backend directory is in PYTHONPATH or accessible
import sys
from pathlib import Path

# Add the parent directory of 'alembic' (i.e., 'backend') to sys.path
# so that 'models' can be imported directly.
sys.path.append(str(Path(__file__).resolve().parents[1]))

from models import Base # Assuming your models.py defines Base in backend/models.py
target_metadata = Base.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired: 
# my_important_option = config.get_main_option("my_important_option")
# ... etc.

def get_url():
    # Try to get DATABASE_URL from environment variables first
    # This is crucial for Dockerized setup where .env is loaded by the app/entrypoint
    db_url = os.getenv("DATABASE_URL")
    if not db_url:
        # Fallback for local alembic commands if .env isn't loaded in this specific context
        # This part might need adjustment based on how you run alembic locally vs in Docker
        print("DATABASE_URL not found in environment, attempting to load from .env for Alembic...")
        from dotenv import load_dotenv
        # Assuming alembic commands are run from the 'backend' directory where .env and alembic.ini are
        dotenv_path = Path(__file__).resolve().parents[1] / '.env'
        if dotenv_path.exists():
            load_dotenv(dotenv_path=dotenv_path)
            db_url = os.getenv("DATABASE_URL")
        else:
            print(f".env file not found at {dotenv_path}, using default fallback URL for Alembic.")
            # Default fallback if .env is not available at all (should not happen in Docker)
            db_url = "postgresql://museum_user:museum_password@localhost:5432/museum_db"
    return db_url

def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = get_url()
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        # include_schemas=True, # if you use schemas
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    # Get the sqlalchemy.url from the alembic.ini section, but override with get_url()
    # This ensures that the environment variable (especially in Docker) takes precedence.
    # configuration = config.get_section(config.config_ini_section)
    # configuration["sqlalchemy.url"] = get_url()
    
    # Create engine configuration dictionary
    engine_config = {
        "sqlalchemy.url": get_url(),
        # Add other engine parameters if needed, e.g., from alembic.ini
    }

    connectable = engine_from_config(
        # configuration, # Pass the modified configuration
        engine_config, # Pass the constructed engine_config directly
        prefix="sqlalchemy.", # This prefix is usually for alembic.ini, adjust if not using it for engine_from_config
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, 
            target_metadata=target_metadata,
            # compare_type=True, # To detect column type changes
            # include_schemas=True, # if you use schemas
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    print("Running migrations offline...")
    run_migrations_offline()
else:
    print("Running migrations online...")
    run_migrations_online()
