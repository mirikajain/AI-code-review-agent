from flask import Blueprint, jsonify

from services.history_service import (
    get_all_history,
    get_history,
    delete_history,
    clear_history
)

history_bp = Blueprint("history", __name__)

@history_bp.route("/history", methods=["GET"])
def history():

    return jsonify({
        "success": True,
        "history": get_all_history()
    })

@history_bp.route("/history/<history_id>", methods=["GET"])
def single_history(history_id):

    history = get_history(history_id)

    if history is None:

        return jsonify({
            "success": False,
            "message": "History not found"
        }),404

    return jsonify({
        "success": True,
        "history": history
    })

@history_bp.route("/history/<history_id>", methods=["DELETE"])
def remove_history(history_id):

    if delete_history(history_id):

        return jsonify({
            "success": True,
            "message": "Deleted"
        })

    return jsonify({
        "success": False,
        "message": "History not found"
    }),404


@history_bp.route("/history", methods=["DELETE"])
def remove_all():

    clear_history()

    return jsonify({
        "success": True,
        "message": "History cleared"
    })