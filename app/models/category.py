import uuid
from sqlalchemy.types import String
from .database import db

class Category(db.Model):
    __tablename__ = "categories"

    id = db.Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(100), nullable=False, unique=True)

    def __repr__(self):
        return f"<Category {self.name}>"

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name
        }
