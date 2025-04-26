from flask import Blueprint

api = Blueprint("api", __name__, url_prefix="/api")


def register_views_and_models():
    from . import views
    from . import models


register_views_and_models()
