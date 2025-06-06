from fastapi import APIRouter

from api.endpoints import auth, categories, pieces_of_art

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(categories.router, prefix="/categories", tags=["Categories"])
api_router.include_router(pieces_of_art.router, prefix="/pieces", tags=["Pieces of Art"])
