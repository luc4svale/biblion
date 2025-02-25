import uuid
from sqlalchemy.types import String
from .database import db

class Author(db.Model):
    __tablename__ = "authors"

    id = db.Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(150), nullable=False, unique=True)

    def __repr__(self):
        return f"<Author {self.name}>"

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name
        }
