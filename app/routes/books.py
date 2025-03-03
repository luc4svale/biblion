from flask import Blueprint, render_template
from flask_login import login_required, current_user

books_bp = Blueprint("books", __name__)

COMMON_TEMPLATE_PATH = "private/pages"


@books_bp.route("/book", methods=["GET"])
@login_required
def render_books():
    return render_template(f"{COMMON_TEMPLATE_PATH}/books/index.html", user=current_user)


@books_bp.route("/home", methods=["GET"])
@login_required
def home():
    return render_template(f"{COMMON_TEMPLATE_PATH}/home/index.html", user=current_user, show_search=True)


@books_bp.route("/book-details", methods=["GET"])
@login_required
def book_details():
    return render_template(f"{COMMON_TEMPLATE_PATH}/book-details/index.html", user=current_user)


@books_bp.route("/favorites", methods=["GET"])
@login_required
def favorites():
    return render_template(f"{COMMON_TEMPLATE_PATH}/favorites/index.html", user=current_user, show_search=True)


@books_bp.route("/reading", methods=["GET"])
@login_required
def reading():
    return render_template(f"{COMMON_TEMPLATE_PATH}/reading/index.html", user=current_user)
