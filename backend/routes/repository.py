from flask import Blueprint, jsonify

from config import REPO_FOLDER
from services.repository_scanner import scan_repository

import os

repository_bp = Blueprint("repository", __name__)


@repository_bp.route("/repository/<repo_id>/files", methods=["GET"])
def list_repository_files(repo_id):

    repo_path = os.path.join(REPO_FOLDER, repo_id)

    if not os.path.exists(repo_path):
        return jsonify({
            "success": False,
            "message": "Repository not found"
        }), 404

    files = scan_repository(repo_path)

    return jsonify({
        "success": True,
        "repo_id": repo_id,
        "total_files": len(files),
        "files": files
    })

from flask import request
from services.file_service import read_file


@repository_bp.route("/repository/<repo_id>/file", methods=["GET"])
def get_file(repo_id):

    relative_path = request.args.get("path")

    if not relative_path:
        return jsonify({
            "success": False,
            "message": "Missing file path"
        }), 400

    repo_path = os.path.join(REPO_FOLDER, repo_id)

    content = read_file(repo_path, relative_path)

    if content is None:
        return jsonify({
            "success": False,
            "message": "File not found or not readable"
        }), 404

    return jsonify({
        "success": True,
        "path": relative_path,
        "content": content
    })