"""
FastAPI Demo Application

This demo showcases the top 5 features of FastAPI:
1. Async Operations
2. Automatic API Documentation
3. Data Validation with Pydantic
4. Dependency Injection
5. WebSocket Support
"""

import asyncio
from typing import List, Optional
from fastapi import FastAPI, Depends, HTTPException, WebSocket, WebSocketDisconnect, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.database import SessionLocal, engine
from app.dependencies import get_db, get_current_user
from app.websocket import ConnectionManager

# Create database tables
models.Base.metadata.create_all(bind=engine)

# Initialize FastAPI application
app = FastAPI(
    title="FastAPI Demo",
    description="Demonstration of FastAPI's top features",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize WebSocket connection manager
manager = ConnectionManager()

# Background task example
async def process_notification(user_id: int, message: str):
    """Simulate a long-running background task."""
    await asyncio.sleep(5)  # Simulate processing
    print(f"Notification processed for user {user_id}: {message}")

@app.post("/users/", response_model=schemas.User)
async def create_user(
    user: schemas.UserCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """
    Create a new user with background task demonstration.
    """
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Create user and add background task
    user = crud.create_user(db=db, user=user)
    background_tasks.add_task(
        process_notification,
        user.id,
        "Welcome to FastAPI Demo!"
    )
    return user

@app.get("/users/", response_model=List[schemas.User])
async def read_users(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Get list of users with pagination.
    """
    users = crud.get_users(db, skip=skip, limit=limit)
    return users

@app.get("/users/{user_id}", response_model=schemas.User)
async def read_user(
    user_id: int,
    db: Session = Depends(get_db)
):
    """
    Get user by ID.
    """
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@app.post("/users/{user_id}/items/", response_model=schemas.Item)
async def create_item_for_user(
    user_id: int,
    item: schemas.ItemCreate,
    current_user: schemas.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Create an item for a user with authentication.
    """
    if current_user.id != user_id:
        raise HTTPException(
            status_code=403,
            detail="Not authorized to create items for other users"
        )
    return crud.create_user_item(db=db, item=item, user_id=user_id)

@app.get("/items/", response_model=List[schemas.Item])
async def read_items(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Get list of items with pagination.
    """
    items = crud.get_items(db, skip=skip, limit=limit)
    return items

@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int):
    """
    WebSocket endpoint for real-time communication.
    """
    await manager.connect(websocket, client_id)
    try:
        while True:
            data = await websocket.receive_text()
            # Broadcast message to all connected clients
            await manager.broadcast(f"Client {client_id}: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket, client_id)
        await manager.broadcast(f"Client {client_id} left the chat")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)