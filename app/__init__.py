from flask import Flask
from flask_migrate import Migrate
from config import Config
from .models.database import db
from .routes import init_routes

Migrate = Migrate()

def create_app():
    """Factory function to create and configure the Flask application"""
    app = Flask(__name__, static_folder='static', template_folder='templates')
    app.config.from_object(Config)

    db.init_app(app)
    Migrate.init_app(app, db)

    init_routes(app)

    return app
