from flask import Blueprint, request, render_template, jsonify, redirect
from flask_login import login_required, current_user, logout_user
from app.controllers import AuthController
from app.utils.decorators import logout_required

auth_controller = AuthController()

COMMON_TEMPLATE_PATH = "public/pages"

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/", methods=["GET"])
@logout_required
def welcome():
    return render_template(f"{COMMON_TEMPLATE_PATH}/welcome/index.html")


@auth_bp.route("/register", methods=["GET", "POST"])
@logout_required
def register():
    if request.method == "POST":
        user_data = request.form
        response = auth_controller.register_user(user_data)
        return jsonify(response), response["status"]
    return render_template(f"{COMMON_TEMPLATE_PATH}/register/index.html")


@auth_bp.route("/login", methods=["GET", "POST"])
@logout_required
def login():
    if request.method == "POST":
        user_data = request.form
        response = auth_controller.login_user(user_data)
        return jsonify(response), response["status"]
    return render_template(f"{COMMON_TEMPLATE_PATH}/login/index.html")


@auth_bp.route("/forgot-password", methods=["GET", "POST"])
@logout_required
def forgot_password():
    if request.method == "POST":
        data = request.form
        return jsonify({"message": "Instruções de redefinição de senha enviadas!", "data": data})
    return render_template(f"{COMMON_TEMPLATE_PATH}/forgot-password/index.html")


@auth_bp.route("/logout", methods=["GET"])
@login_required
def logout():
    if current_user.is_authenticated:
        logout_user()
    return redirect("/login")
