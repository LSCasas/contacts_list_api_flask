from flask import Flask
from .config import Config
from flask_migrate import Migrate
from .db import db
from .api import api


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    app.register_blueprint(api)

    migrate = Migrate(app, db)
    return app
