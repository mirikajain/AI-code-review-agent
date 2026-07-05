from flask import Blueprint, request, jsonify

from services.review_service import review_repository

review_bp = Blueprint("review", __name__)


@review_bp.route("/review", methods=["POST"])
def review():

    data = request.get_json()

    repo_id = data.get("repo_id")
    query = data.get("query")

    if not repo_id or not query:
        return jsonify({
            "error": "repo_id and query are required."
        }), 400

    result = review_repository(repo_id, query)

    return jsonify(result)