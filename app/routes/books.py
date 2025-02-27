from flask import Blueprint, render_template

books_bp = Blueprint("books", __name__)

@books_bp.route("/home", methods=["GET"])
def home():
    return render_template("private/home.html")

@books_bp.route("/book-details", methods=["GET"])
def book_details():
    return render_template("private/book-details.html")

@books_bp.route("/favorites", methods=["GET"])
def favorites():
    return render_template("private/favorites.html")

@books_bp.route("/reading", methods=["GET"])
def reading():
    return render_template("private/reading.html")
