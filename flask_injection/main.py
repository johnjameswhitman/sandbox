"""Demo of basic async tasks for a Flask app.

Run this with:
```shell
python -m main config.prod.Config
```
"""
import sys

from flask import Flask

from api import v1_endpoints


##############################################################################
# This is all that you'd have in main.py.
def create_app(config: str) -> Flask:
    """App factory."""
    app = Flask(__name__)
    app.config.from_object(config)
    app.register_blueprint(v1_endpoints)
    return app


if __name__ == "__main__":
    if len(sys.argv) > 1:
        config = sys.argv[1]
    else:
        config = "config.testing.Config"

    app = create_app(config)
    app.run(debug=True)
