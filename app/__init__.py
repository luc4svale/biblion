from flask import Flask
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from config import Config
from .models import db
from .routes import auth_bp, books_bp, users_bp

def create_app():
    """Factory function to create and configure the Flask application"""
    app = Flask(__name__, static_folder='static', template_folder='templates')
    app.config.from_object(Config)

    db.init_app(app)
    Migrate(app, db)
    Bcrypt(app)

    app.register_blueprint(auth_bp)
    app.register_blueprint(books_bp)
    app.register_blueprint(users_bp)

    return app
