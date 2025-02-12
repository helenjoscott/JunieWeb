# Django Demo Project

This demo showcases the top 5 features of Django and demonstrates PyCharm's superior Django development capabilities.

## Features Demonstrated

### 1. Authentication and User Management
- Custom User Model
- Registration and Login System
- Password Reset Functionality
- User Profile Management
- Permission System

### 2. Admin Interface
- Customized Admin Panel
- Custom Admin Actions
- Inline Model Administration
- List Filters and Search
- Admin Documentation

### 3. ORM and Database Operations
- Complex QuerySets
- Model Relationships
- Database Migrations
- Aggregation and Annotation
- Raw SQL Integration

### 4. Forms and Validation
- Model Forms
- Custom Form Validation
- Form Widgets
- File Upload Handling
- CSRF Protection

### 5. Template Engine and Static Files
- Template Inheritance
- Custom Template Tags
- Static Files Management
- Template Context Processors
- Template Filters

## PyCharm Advantages

### Django-specific Features
1. Django Console
   - Interactive Django shell with code completion
   - Direct database queries
   - Model exploration

2. Template Language Support
   - Syntax highlighting
   - Code completion for template tags
   - Quick documentation
   - Navigate to template declaration

3. Management Commands
   - Run configurations for manage.py
   - Command-line tools integration
   - Custom command support

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

3. Run migrations:
```bash
python manage.py migrate
```

4. Create superuser:
```bash
python manage.py createsuperuser
```

5. Run development server:
```bash
python manage.py runserver
```

## Project Structure
```
django_demo/
├── manage.py
├── requirements.txt
├── static/
├── templates/
└── demo_project/
    ├── __init__.py
    ├── settings.py
    ├── urls.py
    └── wsgi.py
```