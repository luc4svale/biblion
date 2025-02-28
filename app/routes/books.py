from flask import Blueprint, render_template
from flask_login import login_required

books_bp = Blueprint("books", __name__)


@books_bp.route("/home", methods=["GET"])
@login_required
def home():
    return render_template("private/home.html")


@books_bp.route("/book-details", methods=["GET"])
@login_required
def book_details():
    return render_template("private/book-details.html")


@books_bp.route("/favorites", methods=["GET"])
@login_required
def favorites():
    return render_template("private/favorites.html")


@books_bp.route("/reading", methods=["GET"])
@login_required
def reading():
    return render_template("private/reading.html")
