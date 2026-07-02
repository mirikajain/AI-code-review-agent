from flask import Blueprint, request, jsonify
from services.github_service import clone_repository

github_bp = Blueprint("github", __name__)

@github_bp.route("/clone", methods=["POST"])
def clone_repo():
    

    data = request.get_json()

    if not data or "repo_url" not in data:
        return jsonify({
            "success": False,
            "message": "Repository URL is required."
        }), 400

    repo_url = data["repo_url"]

    result = clone_repository(repo_url)
    

    if result["success"]:
        return jsonify(result), 200

    return jsonify(result), 500