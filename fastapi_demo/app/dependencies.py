"""
Dependencies for the FastAPI demo application.
"""

from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import get_db
from .security import decode_token

# OAuth2 scheme for token authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> models.User:
    """
    Dependency to get the current authenticated user.
    Validates the JWT token and returns the user.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = decode_token(token)
        if payload is None:
            raise credentials_exception
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = schemas.TokenData(username=username)
    except JWTError:
        raise credentials_exception

    user = crud.get_user_by_username(db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(
    current_user: models.User = Depends(get_current_user)
) -> models.User:
    """
    Dependency to get the current active user.
    Checks if the user is active.
    """
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )
    return current_user


def get_item_by_id(
    item_id: int,
    db: Session = Depends(get_db)
) -> models.Item:
    """
    Dependency to get an item by ID.
    Raises 404 if item not found.
    """
    item = crud.get_item(db, item_id)
    if item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item not found"
        )
    return item


async def check_item_owner(
    item: models.Item = Depends(get_item_by_id),
    current_user: models.User = Depends(get_current_user)
) -> models.Item:
    """
    Dependency to check if the current user owns the item.
    Raises 403 if user is not the owner.
    """
    if item.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    return item


def get_pagination_params(
    skip: int = 0,
    limit: int = 100
) -> tuple[int, int]:
    """
    Dependency to get pagination parameters.
    Validates and returns skip and limit values.
    """
    if skip < 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Skip parameter must be non-negative"
        )
    if limit < 1:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Limit parameter must be positive"
        )
    if limit > 100:
        limit = 100  # Maximum limit
    return skip, limit