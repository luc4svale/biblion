from flask import Flask
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from config import Config
from .models import db, User
from .routes import auth_bp, books_bp, users_bp, categories_bp, uploads_bp, authors_bp, publishers_bp, favorites_bp

bcrypt = Bcrypt()
login_manager = LoginManager()


def create_app():
    """Factory function to create and configure the Flask application"""
    app = Flask(__name__, static_folder='static', template_folder='templates')
    app.config.from_object(Config)

    db.init_app(app)
    Migrate(app, db)

    bcrypt.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"

    app.register_blueprint(auth_bp)
    app.register_blueprint(users_bp)
    app.register_blueprint(books_bp)
    app.register_blueprint(authors_bp)
    app.register_blueprint(publishers_bp)
    app.register_blueprint(categories_bp)
    app.register_blueprint(favorites_bp)
    app.register_blueprint(uploads_bp)


    return app


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)
