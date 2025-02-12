"""
Flask application factory and extension initialization.
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt
from flask_cors import CORS

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
jwt = JWTManager()
bcrypt = Bcrypt()

def create_app(config_object='config.Config'):
    """
    Application factory function.
    Creates and configures the Flask application.
    """
    app = Flask(__name__)
    app.config.from_object(config_object)

    # Initialize extensions with app
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    jwt.init_app(app)
    bcrypt.init_app(app)
    CORS(app)

    # Configure login manager
    login_manager.login_view = 'auth.login'
    login_manager.login_message_category = 'info'

    # Register blueprints
    from .routes.main import main_bp
    from .routes.auth import auth_bp
    from .routes.api import api_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(api_bp, url_prefix='/api')

    # Register error handlers
    from .utils.error_handlers import register_error_handlers
    register_error_handlers(app)

    # Shell context processor
    @app.shell_context_processor
    def make_shell_context():
        return {
            'db': db,
            'User': User,
            'Item': Item
        }

    return app

# Import models after db is defined
from .models import User, Item