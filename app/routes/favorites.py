from flask import Blueprint, request, render_template, jsonify
from flask_login import login_required, current_user
from app.controllers import FavoriteController

favorite_controller = FavoriteController()

COMMON_TEMPLATE_PATH = "private/pages"

favorites_bp = Blueprint("favorites", __name__)


@favorites_bp.route("/favorite", methods=["POST"])
@login_required
def register_favorite():
    data = request.get_json()
    book_id = data.get("book_id")
    response = favorite_controller.register_favorite(current_user.id, book_id)
    return jsonify(response), response["status"]


@favorites_bp.route("/favorites", methods=["GET"])
@login_required
def render_user_favorites():
    favorites = favorite_controller.get_user_favorites(current_user.id)

    return render_template(
        f"{COMMON_TEMPLATE_PATH}/favorites/index.html",
        user=current_user,
        favorites=favorites
    )


@favorites_bp.route("/favorite/<favorite_id>", methods=["DELETE"])
@login_required
def remove_favorite(favorite_id):
    response = favorite_controller.remove_favorite(favorite_id)
    return jsonify(response), response["status"]
