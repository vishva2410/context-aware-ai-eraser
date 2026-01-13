from flask import Blueprint, jsonify

api_routes = Blueprint("api_routes", __name__)

@api_routes.route("/", methods=["GET"])
def health():
    return jsonify({
        "status": "ok",
        "message": "Backend is running"
    })
