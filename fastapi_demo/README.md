# FastAPI Demo Project

This demo showcases the top 5 features of FastAPI and demonstrates PyCharm's superior Python web development capabilities.

## Features Demonstrated

### 1. Async Operations
- Async route handlers
- Background tasks
- Async database operations
- Concurrent request handling
- Long-running operations management

### 2. Automatic API Documentation
- Interactive API documentation (Swagger UI)
- ReDoc integration
- OpenAPI schema generation
- API versioning
- Custom documentation

### 3. Data Validation with Pydantic
- Request/Response models
- Complex data validation
- Custom validators
- Schema serialization
- Field constraints and types

### 4. Dependency Injection
- Path operation dependencies
- Global dependencies
- Sub-dependencies
- Dependency overrides
- Scoped dependencies

### 5. WebSocket Support
- Real-time communication
- WebSocket endpoints
- Connection management
- Broadcasting messages
- Error handling

## PyCharm Advantages

### FastAPI-specific Features
1. HTTP Client Tools
   - Built-in HTTP client
   - Request history
   - Environment variables
   - Response handling

2. Python Type Hints
   - Type checking
   - Auto-completion
   - Quick documentation
   - Error detection

3. Debugging Tools
   - Async code debugging
   - Breakpoint management
   - Variable inspection
   - Stack trace navigation

### Setup Instructions

1. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install requirements:
```bash
pip install -r requirements.txt
```

3. Run the development server:
```bash
uvicorn main:app --reload
```

4. Access the documentation:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Project Structure
```
fastapi_demo/
├── app/
│   ├── __init__.py
│   ├── models.py          # SQLAlchemy models
│   ├── schemas.py         # Pydantic models
│   ├── crud.py           # Database operations
│   ├── database.py       # Database configuration
│   ├── dependencies.py   # FastAPI dependencies
│   ├── security.py       # Authentication utilities
│   └── websocket.py      # WebSocket manager
├── main.py               # FastAPI application
├── requirements.txt      # Project dependencies
└── README.md            # Project documentation
```

## API Examples

### User Management
```python
# Create user
POST /users/
{
    "email": "user@example.com",
    "username": "testuser",
    "password": "secretpass"
}

# Get user
GET /users/{user_id}

# List users with pagination
GET /users/?skip=0&limit=10
```

### Item Management
```python
# Create item for user
POST /users/{user_id}/items/
{
    "title": "Test Item",
    "description": "This is a test item"
}

# List all items
GET /items/?skip=0&limit=10

# Get user items
GET /users/{user_id}/items/
```

### WebSocket Chat
```python
# Connect to chat
ws://localhost:8000/ws/{client_id}

# Send message
{"message": "Hello, World!"}

# Receive broadcast messages
{"client_id": 1, "message": "Hello, World!", "timestamp": "2023-11-12T10:30:00Z"}
```

Each endpoint demonstrates different FastAPI features including async operations, data validation, dependency injection, and WebSocket support.
