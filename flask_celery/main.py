"""Demo of basic async tasks for a Flask app.

Run this with:
```shell
python -m pip install flask~=1.1  # with flask v2 consider asyncio
python -m main

# In another shell:
wget http://localhost:5000/v0/sleepy

# Back in app shell, observe that the request returns immediately...
# Hi from sleepy
# 127.0.0.1 - - [04/Dec/2021 13:19:33] "GET /v0/sleepy HTTP/1.1" 200 -
# ...then a few seconds later the app logs:
# Hi from slow_task #1
# Hi from slow_task_callback. I got 2.
# Hi from slow_task #0
# Hi from slow_task_callback. I got 1.
# Hi from slow_task #2
# Hi from slow_task_callback. I got 3.
# Hi from slow_task #4
# Hi from slow_task_callback. I got 5.
# Hi from slow_task #3
# Hi from slow_task_callback. I got 4.
```
"""
import os
import time

from celery import Celery
from flask import Flask, Blueprint


##############################################################################
# Normally this would go into something like extensions/celery.py

def make_celery(app: Flask = None) -> Celery:
    """Stands up a Celery instance."""
    if app:
        name = app.import_name
        backend = app.config['CELERY_RESULT_BACKEND']
        broker = app.config['CELERY_BROKER_URL']
    else:
        name = "demo_celery"
        backend = os.environ['CELERY_RESULT_BACKEND']
        broker = os.environ['CELERY_BROKER_URL']

    return Celery(name, backend=backend, broker=broker)
    # celery.conf.update(app.config)


celery = make_celery()


@celery.task()
def worker_task(i: int, request_id: int) -> int:
    """The slow task."""
    time.sleep(2)
    print(
        f"Hi from slow_task #{i} in request {request_id} in PID {os.getpid()}"
    )
    return i + 1


##############################################################################
# Normally this would go into something like endpoints.py
endpoints = Blueprint('v0', __name__, url_prefix='/v0')


REQUEST_ID = {"counter": 0}


@endpoints.route("/do_work")
def do_work() -> dict:
    """Starts a slow async task without blocking request."""
    slow_tasks = 5  # int(request.get_json().get("slow_tasks", 5))
    REQUEST_ID["counter"] += 1
    for i in range(slow_tasks):
        worker_task.delay(i, REQUEST_ID["counter"])

    print(
        f"Hi from sleepy request {REQUEST_ID['counter']} in PID {os.getpid()}"
    )
    return {"status": "ok", "request_id": REQUEST_ID["counter"]}


##############################################################################
# This is all that you'd have in main.py.
def create_app() -> Flask:
    """App factory."""
    app = Flask(__name__)
    app.register_blueprint(endpoints)
    return app


if __name__ == "__main__":
    app = create_app()
    # app.config.update(
    #     CELERY_BROKER_URL='redis://localhost:6379',
    #     CELERY_RESULT_BACKEND='redis://localhost:6379',
    # )

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask

    app.run(debug=True)
