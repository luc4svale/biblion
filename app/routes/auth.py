from flask import Blueprint, request, render_template, jsonify
from app.controllers.auth_controller import AuthController

auth_controller = AuthController()

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/", methods=["GET"])
def index():
    return render_template("public/index.html")

@auth_bp.route("/register", methods=["GET"])
def register_form():
    return render_template("public/register.html")

@auth_bp.route("/register", methods=["POST"])
def register():
    user_data = request.form
    response = auth_controller.register_user(user_data)
    return jsonify(response), response["status"]

@auth_bp.route("/login", methods=["GET"])
def login_form():
    return render_template("public/login.html")

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.form
    return jsonify({"message": "Login realizado!", "data": data})

@auth_bp.route("/forgot-password", methods=["GET"])
def forgot_password_form():
    return render_template("public/forgot-password.html")

@auth_bp.route("/forgot-password", methods=["POST"])
def forgot_password():
    data = request.form
    return jsonify({"message": "Instruções de redefinição de senha enviadas!", "data": data})
