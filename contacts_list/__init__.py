from flask import Flask


def create_app():
    app = Flask(__name__)

    @app.route("/")
    def init():
        return "Server is living"

    return app
