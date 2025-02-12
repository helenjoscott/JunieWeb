"""
Application entry point for the Flask demo application.
"""

import os
from app import create_app

# Create application instance
app = create_app(os.getenv('FLASK_CONFIG', 'default'))


@app.shell_context_processor
def make_shell_context():
    """Configure Flask shell context."""
    from app import db
    from app.models import User, Item
    return {
        'db': db,
        'User': User,
        'Item': Item
    }


if __name__ == '__main__':
    app.run()