from flask import Blueprint, jsonify, request
import os
from werkzeug.utils import secure_filename

from core.pipeline import run_pipeline

api_routes = Blueprint("api_routes", __name__)

UPLOAD_FOLDER = "samples/input"
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@api_routes.route("/", methods=["GET"])
def health():
    return jsonify({
        "status": "ok",
        "message": "Backend is running"
    })


@api_routes.route("/upload", methods=["POST"])
def upload_image():
    # 1️⃣ Check file exists
    if "file" not in request.files:
        return jsonify({"error": "No image file provided"}), 400

    file = request.files["file"]

    # 2️⃣ Validate filename
    if file.filename == "":
        return jsonify({"error": "Empty filename"}), 400

    if not allowed_file(file.filename):
        return jsonify({"error": "Unsupported file type"}), 400

    # 3️⃣ Save file
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    filename = secure_filename(file.filename)
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(file_path)

    # 4️⃣ Run pipeline
    result = run_pipeline(file_path)

    # 5️⃣ Return response
    return jsonify({
        "status": "success",
        "filename": filename,
        "detections": result["detections"],
        "output_image": result["output_image"]
    }), 200
