from flask import Blueprint,request, render_template, redirect, jsonify
from flask_login import current_user
from app.utils.decorators import admin_required
from app.controllers.author_controller import AuthorController

author_controller = AuthorController()

COMMON_TEMPLATE_PATH = "private/pages"

authors_bp = Blueprint("authors", __name__)


@authors_bp.route("/author", methods=["POST"])
@admin_required
def register_author():
    author_data = request.form
    response = author_controller.resgiter_author(author_data)
    return jsonify(response), response["status"]


@authors_bp.route("/author", methods=["GET"])
@admin_required
def render_authors():
    response = author_controller.get_all_authors()
    if response["status"] == 200:
        print(response["data"]["authors"])
        return render_template(f"{COMMON_TEMPLATE_PATH}/authors/index.html", user=current_user, authors=response["data"]["authors"])
    return redirect("/home")


@authors_bp.route("/author/<author_id>", methods=["GET"])
@admin_required
def get_author(author_id):
    response = author_controller.get_author(author_id)
    return jsonify(response), response["status"]


@authors_bp.route("/author/<author_id>", methods=["PUT"])
@admin_required
def edit_author(author_id):
    author_data = request.form
    response = author_controller.edit_author(author_id, author_data)
    return jsonify(response), response["status"]


@authors_bp.route("/author/<author_id>", methods=["DELETE"])
@admin_required
def delete_author(author_id):
    response = author_controller.delete_author(author_id)
    return jsonify(response), response["status"]
