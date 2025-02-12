"""
Pydantic models for request/response validation.
"""

from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, EmailStr, constr


class ItemBase(BaseModel):
    """Base Pydantic model for Item."""
    title: constr(min_length=1, max_length=100)
    description: Optional[str] = None


class ItemCreate(ItemBase):
    """Pydantic model for creating an Item."""
    pass


class Item(ItemBase):
    """Pydantic model for Item responses."""
    id: int
    owner_id: int
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        """Configure Pydantic to work with SQLAlchemy models."""
        from_attributes = True


class UserBase(BaseModel):
    """Base Pydantic model for User."""
    email: EmailStr
    username: constr(min_length=3, max_length=50)


class UserCreate(UserBase):
    """Pydantic model for creating a User."""
    password: constr(min_length=8)


class UserUpdate(BaseModel):
    """Pydantic model for updating a User."""
    email: Optional[EmailStr] = None
    username: Optional[constr(min_length=3, max_length=50)] = None
    password: Optional[constr(min_length=8)] = None


class User(UserBase):
    """Pydantic model for User responses."""
    id: int
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime]
    items: List[Item] = []

    class Config:
        """Configure Pydantic to work with SQLAlchemy models."""
        from_attributes = True


class Token(BaseModel):
    """Pydantic model for JWT tokens."""
    access_token: str
    token_type: str


class TokenData(BaseModel):
    """Pydantic model for JWT token payload."""
    username: Optional[str] = None


class WebSocketMessage(BaseModel):
    """Pydantic model for WebSocket messages."""
    client_id: int
    message: str
    timestamp: datetime = datetime.now()