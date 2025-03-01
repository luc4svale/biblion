from flask import Blueprint, render_template
from flask_login import login_required
from app.models import Book

books_bp = Blueprint("books", __name__)


@books_bp.route("/home", methods=["GET"])
@login_required
def home():
    books = Book.query.all() 
    return render_template("private/home.html", books=books)

@books_bp.route("/book-details", methods=["GET"])
@login_required
def book_details(book_id):
    book = Book.query.get_or_404(book_id)
    return render_template("private/book-details.html", book=book)


@books_bp.route("/favorites", methods=["GET"])
@login_required
def favorites():
    return render_template("private/favorites.html")


@books_bp.route("/reading", methods=["GET"])
@login_required
def reading():
    return render_template("private/reading.html")

@books_bp.route("/book-register", methods=["GET"])
@login_required
def book_register():
    return render_template("private/book-register.html")

