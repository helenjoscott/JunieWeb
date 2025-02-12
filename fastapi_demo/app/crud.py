"""
CRUD operations for the FastAPI demo application.
"""

from sqlalchemy.orm import Session
from . import models, schemas
from .security import get_password_hash


def get_user(db: Session, user_id: int):
    """Get a user by ID."""
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    """Get a user by email."""
    return db.query(models.User).filter(models.User.email == email).first()


def get_user_by_username(db: Session, username: str):
    """Get a user by username."""
    return db.query(models.User).filter(models.User.username == username).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    """Get a list of users with pagination."""
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    """Create a new user."""
    hashed_password = get_password_hash(user.password)
    db_user = models.User(
        email=user.email,
        username=user.username,
        hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def update_user(db: Session, user_id: int, user: schemas.UserUpdate):
    """Update a user's information."""
    db_user = get_user(db, user_id)
    if not db_user:
        return None
    
    update_data = user.dict(exclude_unset=True)
    if "password" in update_data:
        update_data["hashed_password"] = get_password_hash(update_data.pop("password"))
    
    for field, value in update_data.items():
        setattr(db_user, field, value)
    
    db.commit()
    db.refresh(db_user)
    return db_user


def delete_user(db: Session, user_id: int):
    """Delete a user."""
    db_user = get_user(db, user_id)
    if not db_user:
        return None
    
    db.delete(db_user)
    db.commit()
    return db_user


def get_item(db: Session, item_id: int):
    """Get an item by ID."""
    return db.query(models.Item).filter(models.Item.id == item_id).first()


def get_items(db: Session, skip: int = 0, limit: int = 100):
    """Get a list of items with pagination."""
    return db.query(models.Item).offset(skip).limit(limit).all()


def get_user_items(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    """Get a list of items for a specific user."""
    return (db.query(models.Item)
            .filter(models.Item.owner_id == user_id)
            .offset(skip)
            .limit(limit)
            .all())


def create_user_item(db: Session, item: schemas.ItemCreate, user_id: int):
    """Create a new item for a user."""
    db_item = models.Item(**item.dict(), owner_id=user_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def update_item(db: Session, item_id: int, item: schemas.ItemBase):
    """Update an item's information."""
    db_item = get_item(db, item_id)
    if not db_item:
        return None
    
    update_data = item.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_item, field, value)
    
    db.commit()
    db.refresh(db_item)
    return db_item


def delete_item(db: Session, item_id: int):
    """Delete an item."""
    db_item = get_item(db, item_id)
    if not db_item:
        return None
    
    db.delete(db_item)
    db.commit()
    return db_item