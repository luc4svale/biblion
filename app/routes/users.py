from flask import Blueprint, request, render_template, redirect, jsonify
from flask_login import login_required, current_user
from app.controllers.user_controller import UserController

user_controller = UserController()

users_bp = Blueprint("users", __name__)

@users_bp.route("/profile", methods=["GET"])
@login_required
def render_profile():
    user_profile = user_controller.get_user_profile(current_user.id)
    if user_profile["status"] == 200:
        return render_template("private/profile.html", user=user_profile["data"])
    if current_user.is_authenticated:
        return redirect("/logout")
    return redirect("/login")


@users_bp.route("/profile", methods=["PUT"])
@login_required
def change_personal_info():
    user_data = request.form.to_dict()

    photo = request.files.get("photo", None)
    user_data["photo"] = photo if photo and photo.filename else None

    print(user_data["photo"])
    response = user_controller.change_user_personal_info(current_user.id, user_data)
    return jsonify(response), response["status"]
