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
    file_path = db.Column(db.String(255), nullable=False)  # Caminho do arquivo no sistema
    cover_image_path = db.Column(db.String(255))  # Caminho da capa do livro

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
            "file_path": self.file_path,
            "cover_image_path": self.cover_image_path,
            "author_id": self.author_id,
            "category_id": self.category_id,
            "publisher_id": self.publisher_id,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }
