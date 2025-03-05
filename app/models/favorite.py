from datetime import datetime, timezone
import uuid
from sqlalchemy.types import String
from .database import db

class Favorite(db.Model):
    __tablename__ = 'favorites'

    id = db.Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    book_id = db.Column(db.String(36), db.ForeignKey('books.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))


    user = db.relationship("User", backref="favorites", lazy=True)
    book = db.relationship("Book", backref="favorited_by", lazy=True)


    def to_dict(self):
        return {
            "id": self.id,
            "user": {"id": self.user.id, "name": self.user.name} if self.user else None,
            "book": {
                "id": self.book.id,
                "title": self.book.title,
                "cover": self.book.cover,
                "author": self.book.author.name if self.book.author else "Desconhecido"
            } if self.book else None,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }
