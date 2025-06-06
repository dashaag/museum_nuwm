from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional, Union
from datetime import datetime

# Base models for common fields
class TimeStampedModel(BaseModel):
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

# Category Schemas
class CategoryBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None

class CategoryCreate(CategoryBase):
    pass

class CategoryUpdate(CategoryBase):
    pass

class Category(CategoryBase, TimeStampedModel):
    id: int

    class Config:
        from_attributes = True # Changed from orm_mode for Pydantic v2

# PieceOfArt Schemas
class PieceOfArtBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    image_url: str = Field(..., max_length=1024) # Assuming URL validation is handled elsewhere or by type
    category_id: int

class PieceOfArtCreate(PieceOfArtBase):
    pass

class PieceOfArtUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    image_url: Optional[str] = Field(None, max_length=1024)
    category_id: Optional[int] = None

class PieceOfArt(PieceOfArtBase, TimeStampedModel):
    id: int
    category: Optional[Category] = None # Include category details when fetching a piece of art

    class Config:
        from_attributes = True

# Manager Schemas
class ManagerBase(BaseModel):
    email: EmailStr
    first_name: str = Field(..., min_length=1, max_length=100)
    last_name: str = Field(..., min_length=1, max_length=100)

class ManagerCreate(ManagerBase):
    password: str = Field(..., min_length=8)

class ManagerUpdate(BaseModel):
    email: Optional[EmailStr] = None
    first_name: Optional[str] = Field(None, min_length=1, max_length=100)
    last_name: Optional[str] = Field(None, min_length=1, max_length=100)
    password: Optional[str] = Field(None, min_length=8)

class Manager(ManagerBase, TimeStampedModel):
    id: int

    class Config:
        from_attributes = True

# Token Schemas for Authentication
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Union[EmailStr, None] = None

# For login form (FastAPI uses this for OAuth2PasswordRequestForm)
# No need to define it here if using FastAPI's form directly in the endpoint
# class LoginRequest(BaseModel):
#     username: EmailStr # FastAPI's OAuth2PasswordRequestForm uses 'username'
#     password: str
