import uuid
from sqlalchemy.types import String
from .database import db

class Favorite(db.Model):
    __tablename__ = 'favorites'

    id = db.Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'), primary_key=True)
