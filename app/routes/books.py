from datetime import datetime
from flask import Blueprint, request, render_template,  jsonify, redirect
from flask_login import login_required, current_user
from app.utils.decorators import admin_required
from app.controllers.book_controller import BookController


book_controller = BookController()

COMMON_TEMPLATE_PATH = "private/pages"

books_bp = Blueprint("books", __name__)


@books_bp.route("/book", methods=["POST"])
@admin_required
def register_book():
    book_data = request.form.to_dict()
    cover = request.files.get("cover", None)
    file = request.files.get("file", None)
    book_data["cover"] = cover if cover and cover.filename else None
    book_data["file"] = file if file and file.filename else None
    response = book_controller.register_book(book_data)
    return jsonify(response), response["status"]


@books_bp.route("/book", methods=["GET"])
@admin_required
def render_books():
    response = book_controller.get_all_books()
    current_year = datetime.now().year
    if response["status"] != 200:
        return redirect("/home")
    return render_template(
        f"{COMMON_TEMPLATE_PATH}/books/index.html",
        user=current_user,
        books=response["data"]["books"],
        current_year=current_year
    )


@books_bp.route("/book/<book_id>", methods=["GET"])
@admin_required
def get_book(book_id):
    response = book_controller.get_book(book_id)
    return jsonify(response), response["status"]



@books_bp.route("/book/<book_id>", methods=["PUT"])
@admin_required
def edit_book(book_id):
    book_data = request.form.to_dict()
    cover = request.files.get("cover", None)
    file = request.files.get("file", None)
    book_data["cover"] = cover if cover and cover.filename else None
    book_data["file"] = file if file and file.filename else None
    response = book_controller.edit_book(book_id, book_data)
    return jsonify(response), response["status"]


@books_bp.route("/book/<book_id>", methods=["DELETE"])
@admin_required
def delete_book(book_id):
    response = book_controller.delete_book(book_id)
    return jsonify(response), response["status"]



@books_bp.route("/home", methods=["GET"])
@login_required
def home():
    response = book_controller.get_books_by_category()

    return render_template(
        f"{COMMON_TEMPLATE_PATH}/home/index.html",
        user=current_user,
        show_search=True,
        books_by_category=response.get("data", {})
    )


@books_bp.route("/details/<book_id>", methods=["GET"])
@login_required
def book_details(book_id):
    response = book_controller.get_book_details(book_id)

    return render_template(
        f"{COMMON_TEMPLATE_PATH}/details/index.html",
        user=current_user,
        book=response.get("data")
)



@books_bp.route("/reading/<book_id>", methods=["GET"])
@login_required
def reading(book_id):
    response = book_controller.get_book_file(book_id)

    return render_template(
        f"{COMMON_TEMPLATE_PATH}/reading/index.html",
        user=current_user,
        book_file=response.get("data")
    )


@books_bp.route("/favorites", methods=["GET"])
@login_required
def favorites():
    return render_template(
        f"{COMMON_TEMPLATE_PATH}/favorites/index.html",
        user=current_user,
        show_search=True
    )
