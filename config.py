import os
from dotenv import load_dotenv

# Load .env variables
load_dotenv()

class Config: # pylint: disable=too-few-public-methods
    SECRET_KEY = os.getenv('SECRET_KEY')
    if not SECRET_KEY:
        raise ValueError("SECRET_KEY is not defined! Verify the environment variables")

    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///db.sqlite3')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
