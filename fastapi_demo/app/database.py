"""
Database configuration and session management.
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLite database URL (for demo purposes)
SQLALCHEMY_DATABASE_URL = "sqlite:///./demo.db"

# Create database engine
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}  # Needed for SQLite
)

# Create SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create Base class for declarative models
Base = declarative_base()

# Database Dependency
def get_db():
    """
    Dependency function to get database session.
    Ensures proper handling of database connections.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()