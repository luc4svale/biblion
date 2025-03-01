from datetime import datetime, timezone
import uuid
from flask_bcrypt import Bcrypt
from flask_login import UserMixin
from sqlalchemy.types import String
from .database import db

bcrypt = Bcrypt()

class User(db.Model, UserMixin):
    __tablename__ = "users"

    id = db.Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False, default="user")
    photo = db.Column(db.String(70), nullable=False, server_default="default-photo.svg")
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime,
                           default=lambda: datetime.now(timezone.utc),
                           onupdate=lambda: datetime.now(timezone.utc))

    def set_password(self, password):
        self.password = bcrypt.generate_password_hash(password).decode("utf-8")

    def to_dict(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "role": self.role,
            "password": self.password,
            "photo": self.photo,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }
