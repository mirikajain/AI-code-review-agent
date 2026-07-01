from flask import Blueprint, request, jsonify
import os

from services.zip_service import save_zip, extract_zip
from config import REPO_FOLDER

upload_bp = Blueprint("upload", __name__)


@upload_bp.route("/upload", methods=["POST"])
def upload_repository():

    # Check if file exists in request
    if "file" not in request.files:
        return jsonify({"success": False, "error": "No file uploaded"}), 400

    file = request.files["file"]

    # Check if filename is empty
    if file.filename == "":
        return jsonify({"success": False, "error": "No file selected"}), 400

    # Allow only ZIP files
    if not file.filename.lower().endswith(".zip"):
        return jsonify({
            "success": False,
            "error": "Only ZIP files are allowed."
        }), 400

    try:
        # Step 1: Save uploaded ZIP temporarily
        zip_path = save_zip(file)

        # Step 2: Extract ZIP into storage/repos/<repo_id>
        repo_id, repo_path = extract_zip(zip_path, REPO_FOLDER)

        # Step 3: Delete temporary ZIP
        if os.path.exists(zip_path):
            os.remove(zip_path)

        return jsonify({
            "success": True,
            "message": "Repository uploaded successfully.",
            "repo_id": repo_id,
            "repository_path": repo_path,
            "source": "zip"
        }), 200

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500