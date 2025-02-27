from flask import Blueprint, render_template

users_bp = Blueprint("users", __name__)

@users_bp.route("/profile", methods=["GET"])
def profile():
    return render_template("private/profile.html")
