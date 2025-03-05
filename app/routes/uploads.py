import os
from flask import Blueprint, send_from_directory
from flask_login import login_required


uploads_bp = Blueprint("uploads", __name__)

UPLOAD_FOLDER = os.path.abspath("uploads/")

@uploads_bp.route("/uploads/profiles/<filename>")
@login_required
def get_profile_image(filename):
    return send_from_directory(f"{UPLOAD_FOLDER}/profiles", filename)


@uploads_bp.route("/uploads/covers/<filename>")
@login_required
def get_cover_image(filename):
    return send_from_directory(f"{UPLOAD_FOLDER}/covers", filename)


@uploads_bp.route("/uploads/books/<filename>")
@login_required
def get_book_file(filename):
    return send_from_directory(f"{UPLOAD_FOLDER}/books", filename)

