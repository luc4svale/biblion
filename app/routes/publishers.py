from flask import Blueprint,request, render_template, redirect, jsonify
from flask_login import current_user
from app.utils.decorators import admin_required
from app.controllers.publisher_controller import PublisherController


publisher_controller = PublisherController()

COMMON_TEMPLATE_PATH = "private/pages"

publishers_bp = Blueprint("publishers", __name__)


@publishers_bp.route("/publisher", methods=["POST"])
@admin_required
def register_publisher():
    publisher_data = request.form
    response = publisher_controller.resgiter_publisher(publisher_data)
    return jsonify(response), response["status"]


@publishers_bp.route("/publisher", methods=["GET"])
@admin_required
def render_publishers():
    response = publisher_controller.get_all_publishers()
    if response["status"] == 200:
        print(response["data"]["publishers"])
        return render_template(f"{COMMON_TEMPLATE_PATH}/publishers/index.html", user=current_user, publishers=response["data"]["publishers"])
    return redirect("/home")


@publishers_bp.route("/publisher/<publisher_id>", methods=["GET"])
@admin_required
def get_publisher(publisher_id):
    response = publisher_controller.get_publisher(publisher_id)
    return jsonify(response), response["status"]


@publishers_bp.route("/publisher/<publisher_id>", methods=["PUT"])
@admin_required
def edit_publisher(publisher_id):
    publisher_data = request.form
    response = publisher_controller.edit_publisher(publisher_id, publisher_data)
    return jsonify(response), response["status"]


@publishers_bp.route("/publisher/<publisher_id>", methods=["DELETE"])
@admin_required
def delete_publisher(publisher_id):
    response = publisher_controller.delete_publisher(publisher_id)
    return jsonify(response), response["status"]
