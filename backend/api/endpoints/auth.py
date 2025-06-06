from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

import crud
import schemas
import security # Renamed from auth to security to avoid module name conflict
from api import deps # For get_db dependency if not directly imported
from core.config import settings
from database import get_db # Direct import for get_db

router = APIRouter()

@router.post("/login", response_model=schemas.Token)
def login_for_access_token(
    db: Session = Depends(get_db),
    form_data: OAuth2PasswordRequestForm = Depends()
):
    """
    OAuth2 compatible token login, get an access token for future requests.
    Username is the manager's email.
    """
    manager = crud.get_manager_by_email(db, email=form_data.username)
    if not manager or not security.verify_password(form_data.password, manager.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = security.create_access_token(
        subject=manager.email, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
