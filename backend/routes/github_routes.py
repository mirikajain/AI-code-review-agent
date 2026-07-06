from flask import Blueprint, request, jsonify
from services.github_service import clone_repository
from services.review_service import analyze_repository

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

    # Clone only once
    result = clone_repository(repo_url)

    if not result["success"]:
        return jsonify(result), 500

    repo_id = result["repo_id"]
    repo_path = result["repository_path"]

    print("Starting repository analysis...")

    analyze_repository(repo_id, repo_path)

    print("Repository analysis completed.")

    return jsonify(result), 200