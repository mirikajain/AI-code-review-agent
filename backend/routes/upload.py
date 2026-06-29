from flask import Blueprint, request, jsonify
from services.zip_service import save_zip

upload_bp = Blueprint("upload", __name__)


@upload_bp.route("/upload", methods=["POST"])
def upload_repository():

    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]

    if file.filename == "":
        return jsonify({"error": "No file selected"}), 400

    filepath = save_zip(file)

    return jsonify({
        "message": "ZIP uploaded successfully",
        "path": filepath
    })