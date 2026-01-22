from flask import Flask, send_from_directory
from api.routes import api_routes

def create_app():
    # Serve static files from the frontend directory
    app = Flask(__name__, static_folder="../frontend", static_url_path="/")
    app.register_blueprint(api_routes)

    @app.route("/")
    def index():
        return app.send_static_file("index.html")

    @app.route("/processed/<path:filename>")
    def serve_processed(filename):
        return send_from_directory("../samples/output", filename)

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
