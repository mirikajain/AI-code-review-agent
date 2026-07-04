from flask import Blueprint, jsonify
import os

from config import REPO_FOLDER
from services.repository_scanner import scan_repository
from services.dependency_parser import parse_dependencies
from services.review_service import analyze_repository
from services.retriever_service import retrieve_chunks

repository_bp = Blueprint("repository", __name__)

@repository_bp.route("/repository/<repo_id>/files", methods=["GET"])
def list_repository_files(repo_id):

    repo_path = os.path.join(REPO_FOLDER, repo_id)

    if not os.path.exists(repo_path):
        return jsonify({
            "success": False,
            "message": "Repository not found"
        }), 404

    scan_result = scan_repository(repo_path)

    return jsonify({
        "success": True,
        "repo_id": repo_id,
        "total_files": scan_result["total_files"],
        "code_files": scan_result["code_files"],
        "metadata_files": scan_result["metadata_files"]
    })

@repository_bp.route("/repository/<repo_id>/dependencies", methods=["GET"])
def get_dependencies(repo_id):

    repo_path = os.path.join(REPO_FOLDER, repo_id)

    if not os.path.exists(repo_path):
        return jsonify({
            "success": False,
            "message": "Repository not found"
        }), 404

    # Step 1: Scan repository
    scan_result = scan_repository(repo_path)

    # Step 2: Parse dependencies
    dependencies = parse_dependencies(
        repo_path,
        scan_result["metadata_files"]
    ) 
    
    return jsonify({
        "success": True,
        "repo_id": repo_id,
        "dependencies": dependencies
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
    
@repository_bp.route("/repository/<repo_id>/analyze", methods=["GET"])
def analyze(repo_id):   
        
        repo_path = os.path.join(REPO_FOLDER, repo_id)

        if not os.path.exists(repo_path):
            return jsonify({
                "success": False,
                "message": "Repository not found"
            }), 404

        result = analyze_repository(repo_id,repo_path)

        return jsonify({
            "success": True,
            "repo_id": repo_id,
            "analysis": result
        })


@repository_bp.route("/repository/<repo_id>/search", methods=["GET"])
def search_repository(repo_id):

    query = request.args.get("query")

    if not query:
        return jsonify({
            "success": False,
            "message": "Missing query"
        }), 400

    results = retrieve_chunks(
        repo_id,
        query
    )

    return jsonify({
        "success": True,
        "results": results
    })