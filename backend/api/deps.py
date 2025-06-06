from typing import Generator, Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from pydantic import EmailStr # For type hinting email in TokenData

from core.config import settings
import crud
import models
import schemas
from database import get_db # Corrected: get_db is the dependency

reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"/api/auth/login" # Ensure this matches your auth router's login path
)

def get_current_manager(db: Session = Depends(get_db), token: str = Depends(reusable_oauth2)) -> models.Manager:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        # The 'sub' in JWT should be the manager's email
        subject: Optional[str] = payload.get("sub")
        if subject is None:
            raise credentials_exception
        # Validate if the subject is a valid email format, though jwt.decode doesn't do this by default
        # Pydantic's EmailStr can be used if you construct a model, e.g. TokenData
        token_data = schemas.TokenData(email=subject)

    except JWTError:
        raise credentials_exception
    except ValueError: # Handles Pydantic validation error for EmailStr
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, # Or 401, depending on desired behavior
            detail="Invalid email format in token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    manager = crud.get_manager_by_email(db, email=token_data.email)
    if manager is None:
        raise credentials_exception # Manager not found in DB
    return manager

# Example of a dependency for a superuser, if you implement roles:
# def get_current_active_superuser(
#     current_manager: models.Manager = Depends(get_current_manager),
# ) -> models.Manager:
#     # Add a check here, e.g., if not current_manager.is_superuser:
#     # This requires an 'is_superuser' attribute or similar on your Manager model or in crud.
#     # For now, this is a placeholder.
#     if not getattr(current_manager, 'is_superuser', False): # Example check
#         raise HTTPException(
#             status_code=status.HTTP_403_FORBIDDEN, 
#             detail="The user doesn't have enough privileges (superuser required)"
#         )
#     return current_manager
