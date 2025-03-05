from datetime import datetime, timezone
import uuid
from sqlalchemy.types import String
from .database import db

class Book(db.Model):
    __tablename__ = "books"

    id = db.Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    title = db.Column(db.String(200), nullable=False)
    synopsis = db.Column(db.Text, nullable=False)
    publication_year = db.Column(db.Integer)
    file = db.Column(db.String(70), nullable=False)
    cover = db.Column(db.String(70), nullable=False, server_default="default-cover.jpg")

    author_id = db.Column(String(36), db.ForeignKey("authors.id"), nullable=False)
    category_id = db.Column(String(36), db.ForeignKey("categories.id"), nullable=False)
    publisher_id = db.Column(String(36), db.ForeignKey("publishers.id"), nullable=False)

    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime,
                           default=lambda: datetime.now(timezone.utc),
                           onupdate=lambda: datetime.now(timezone.utc))

    # Relationships
    author = db.relationship("Author", backref="books")
    category = db.relationship("Category", backref="books")
    publisher = db.relationship("Publisher", backref="books")

    def __repr__(self):
        return f"<Book {self.title} ({self.publication_year})>"

    def to_dict(self):
        return {
        "id": self.id,
        "title": self.title,
        "synopsis": self.synopsis,
        "publication_year": self.publication_year,
        "file": self.file,
        "cover": self.cover,
        "author": {"id": self.author.id, "name": self.author.name} if self.author else None,
        "category": {"id": self.category.id, "name": self.category.name} if self.category else None,
        "publisher": {"id": self.publisher.id, "name": self.publisher.name} if self.publisher else None,
        "created_at": self.created_at.isoformat() if self.created_at else None,
        "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }
