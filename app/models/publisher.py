from datetime import datetime, timezone
import uuid
from sqlalchemy.types import String
from .database import db

class Publisher(db.Model):
    __tablename__ = "publishers"

    id = db.Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(150), nullable=False, unique=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime,
                           default=lambda: datetime.now(timezone.utc),
                           onupdate=lambda: datetime.now(timezone.utc))


    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "created_at": self.created_at.strftime('%d/%m/%Y %H:%M:%S'),
            "updated_at": self.updated_at.strftime('%d/%m/%Y %H:%M:%S'),
        }
