# Flask Demo Project

This demo showcases the top 5 features of Flask and demonstrates PyCharm's superior Python web development capabilities.

## Features Demonstrated

### 1. Routing and Blueprint Organization
- Blueprint registration
- URL routing patterns
- URL parameters
- Request handling
- Response formatting

### 2. RESTful API Implementation
- Resource-based routing
- HTTP methods
- Request parsing
- Response serialization
- API versioning

### 3. Database Integration (SQLAlchemy)
- Model definitions
- Database migrations
- CRUD operations
- Relationships
- Query optimization

### 4. Authentication
- User authentication
- Session management
- Token-based auth
- Role-based access control
- Security features

### 5. Custom Error Handling
- Error pages
- Exception handling
- Logging
- Debugging
- Error reporting

## PyCharm Advantages

### Flask-specific Features
1. Flask Run Configurations
   - Development server settings
   - Environment variables
   - Debug configurations
   - Hot reload support

2. Template Support
   - Jinja2 syntax highlighting
   - Code completion
   - Template navigation
   - Live templates

3. Testing Tools
   - Test runner integration
   - Coverage analysis
   - Test debugging
   - Fixtures support

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

3. Set environment variables:
```bash
export FLASK_APP=app
export FLASK_ENV=development
```

4. Initialize the database:
```bash
flask db upgrade
```

5. Run the development server:
```bash
flask run
```

## Project Structure
```
flask_demo/
├── app/
│   ├── __init__.py
│   ├── models/
│   ├── routes/
│   ├── templates/
│   ├── static/
│   └── utils/
├── tests/
├── config.py
├── requirements.txt
└── run.py
```

## API Examples

### Authentication
```python
# Register new user
POST /auth/register
{
    "username": "testuser",
    "email": "user@example.com",
    "password": "secretpass"
}

# Login user
POST /auth/login
{
    "username": "testuser",
    "password": "secretpass"
}
Response:
{
    "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
    "token_type": "bearer"
}
```

### Item Management
```python
# Create new item
POST /api/items
Headers: Authorization: Bearer <token>
{
    "name": "Test Item",
    "description": "This is a test item",
    "price": 29.99
}

# Get items with pagination
GET /api/items?page=1&per_page=10
Response:
{
    "items": [...],
    "total": 42,
    "page": 1,
    "per_page": 10,
    "pages": 5
}

# Update item
PUT /api/items/<id>
Headers: Authorization: Bearer <token>
{
    "name": "Updated Item",
    "price": 39.99
}
```

### Error Handling Examples
```python
# 404 Not Found
GET /api/items/999
{
    "error": "Item not found",
    "status_code": 404
}

# 401 Unauthorized
POST /api/items
{
    "error": "Missing authorization header",
    "status_code": 401
}

# 400 Bad Request
POST /api/items
{
    "error": "Validation error",
    "status_code": 400,
    "details": {
        "name": ["Field is required"],
        "price": ["Must be a positive number"]
    }
}
```

Each endpoint demonstrates Flask's features including:
- Blueprint organization
- Request validation
- Authentication & authorization
- Database operations
- Error handling
- Response formatting
