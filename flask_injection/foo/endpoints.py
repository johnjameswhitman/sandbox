"""Demo of basic async tasks for a Flask app.

Run this with:
```shell
python -m main config.prod.Config
```
"""
import os

from flask import Blueprint, current_app


endpoints = Blueprint('foos', __name__, url_prefix='/foos')


REQUEST_ID = {"counter": 0}


@endpoints.route("/do_work")
def do_work() -> dict:
    """Starts a slow async task without blocking request."""
    foo_service = current_app.config["FOO_SERVICE_IMPL"](name="do_work_caller")
    tasks = 5  # int(request.get_json().get("slow_tasks", 5))
    REQUEST_ID["counter"] += 1
    for i in range(tasks):
        foo_service.foobobulate(f"Greetings from do_work task {i}!")

    print(
        f"Hi from sleepy request {REQUEST_ID['counter']} in PID {os.getpid()}"
    )
    return {"status": "ok", "request_id": REQUEST_ID["counter"]}
