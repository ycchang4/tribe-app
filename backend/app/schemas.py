from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List, Dict
from datetime import datetime

# User Schemas
class UserBase(BaseModel):
    email: EmailStr
    name: str
    age: Optional[int] = None
    gender: Optional[str] = None
    location: Optional[str] = None
    bio: Optional[str] = None

class UserCreate(UserBase):
    password: str
    life_story: str

class UserResponse(UserBase):
    id: int
    primary_color: Optional[str] = None
    color_scores: Optional[Dict[str, float]] = None
    profile_photo_url: Optional[str] = None
    created_at: datetime
    
    class Config:
        from_attributes = True

# Auth Schemas
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"