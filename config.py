import os
from dotenv import load_dotenv

load_dotenv()

print(os.getenv('DATABASE_URL'))
print(os.getenv('SECRET_KEY'))

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'default_secret_key')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///default.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
