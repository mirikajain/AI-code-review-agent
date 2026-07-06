from flask import Blueprint, request, jsonify

from services.review_service import review_repository

review_bp = Blueprint("review", __name__)


@review_bp.route("/review", methods=["POST"])
def review():

    data = request.get_json()

    repo_id = data["repo_id"]
    print("Review repo_id:", repo_id)

    query = data["query"]

    result = review_repository(repo_id, query)
    print(result)

    return jsonify(result)