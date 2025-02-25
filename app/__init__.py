from flask import Flask
from config import Config

def create_app():
    """Factory function to create and configure the Flask application"""
    app = Flask(__name__, static_folder='static', template_folder='templates')
    app.config.from_object(Config)

    @app.route("/")
    def home():
        return "Flask is running!"

    return app
