from flask import Blueprint,request, render_template, redirect, jsonify
from flask_login import current_user
from app.utils.decorators import admin_required
from app.controllers.category_controller import CategoryController


category_controller = CategoryController()

COMMON_TEMPLATE_PATH = "private/pages/"

categories_bp = Blueprint("categories", __name__)


@categories_bp.route("/category", methods=["GET"])
@admin_required
def render_categories():
    response = category_controller.get_all_categories()
    if response["status"] == 200:
        print(response["data"]["categories"])
        return render_template(f"{COMMON_TEMPLATE_PATH}categories/index.html", user=current_user, categories=response["data"]["categories"])
    return redirect("/home")


@categories_bp.route("/category/<category_id>", methods=["GET"])
@admin_required
def get_category(category_id):
    response = category_controller.get_category(category_id)
    return jsonify(response), response["status"]


@categories_bp.route("/category", methods=["POST"])
@admin_required
def register_category():
    category_data = request.form
    response = category_controller.resgiter_category(category_data)
    return jsonify(response), response["status"]
