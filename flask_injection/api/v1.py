from flask import Blueprint

from foo import endpoints as foo_endpoints


v1_endpoints = Blueprint("v1", __name__, url_prefix="/v1")

v1_endpoints.register_blueprint(foo_endpoints)
