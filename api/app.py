from flask import Flask, send_from_directory
from api.routes import api_routes

import os

def create_app():
    # Use absolute paths for robustness
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    FRONTEND_DIR = os.path.join(BASE_DIR, "frontend")
    OUTPUT_DIR = os.path.join(BASE_DIR, "samples/output")

    # Serve static files from the frontend directory
    app = Flask(__name__, static_folder=FRONTEND_DIR, static_url_path="/")
    app.register_blueprint(api_routes)

    @app.route("/")
    def index():
        return app.send_static_file("index.html")

    @app.route("/processed/<path:filename>")
    def serve_processed(filename):
        return send_from_directory(OUTPUT_DIR, filename)

    return app

# Expose app for gunicorn
app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
