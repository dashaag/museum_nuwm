from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from core.config import settings
from api.api import api_router
# from database import engine, Base # For initial table creation if not using Alembic

# If you were to create tables directly without Alembic (not recommended for production/evolution)
# from database import engine, Base
# from models import Category, PieceOfArt, Manager # Ensure all models are imported
# Base.metadata.create_all(bind=engine) # This line would create tables

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.PROJECT_VERSION,
    openapi_url=f"/api/openapi.json" # Standard location for OpenAPI spec
)

# Set all CORS enabled origins
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.include_router(api_router, prefix="/api")

@app.get("/api/healthcheck")
def healthcheck():
    return {"status": "ok"}

# The initial_data.py script will be run by entrypoint.sh based on INIT_DB env var.
# No need to call it from here directly.
