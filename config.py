import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    INSTANCE_DIR = os.path.join(BASE_DIR, "instance")

    if not os.path.exists(INSTANCE_DIR):
        os.makedirs(INSTANCE_DIR)

    SECRET_KEY = os.getenv('SECRET_KEY')
    if not SECRET_KEY:
        raise ValueError("SECRET_KEY is not defined! Verify the environment variables.")

    DATABASE_URL = os.getenv('DATABASE_URL',
                             f"sqlite:///{os.path.join(INSTANCE_DIR, 'db.sqlite3')}")

    SQLALCHEMY_DATABASE_URI = DATABASE_URL
    SQLALCHEMY_TRACK_MODIFICATIONS = False
