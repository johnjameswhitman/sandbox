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
import atexit
import os
import time
from concurrent.futures import ThreadPoolExecutor
from typing import Optional

from flask import Flask, Blueprint


##############################################################################
# Normally this would go into something like extensions/thread_pool_manager.py
class ThreadPoolManager:
    """Manages a shared thread pool for executing simple async tasks.

    Mostly borrowed from the following docs:
        - https://flask.palletsprojects.com/en/1.1.x/extensiondev/#the-extension-code
        - https://docs.python.org/3.9/library/concurrent.futures.html#threadpoolexecutor

    The Flask docs tie resource-lifecycle to the request lifecycle via the app context;
    however, if you shutdown the threadpool with a "teardown_appcontext" hook, then it
    blocks the request until all of its tasks finish. This is undesired, so tie the
    executor's lifecycle to the ThreadPoolManager instance lifecycle.
    """
    workers: Optional[int] = None
    _executor: Optional[ThreadPoolExecutor] = None

    def __init__(self, app: Optional[Flask] = None):
        print("Hi from thread_pool_manager.__init__")
        self.app = app
        if app is not None:
            self.init_app(app)

    def init_app(self, app: Flask) -> None:
        print("Hi from thread_pool_manager.init_app")
        self.workers = app.config.get("THREAD_POOL_MANAGER_WORKERS")

    @property
    def executor(self) -> ThreadPoolExecutor:
        """Lazily sets up threadpool."""
        if not self._executor:
            self._executor = ThreadPoolExecutor(max_workers=self.workers)
        return self._executor

    def teardown(self) -> None:
        """Cleans up worker pool if it exists."""
        print("Hi from ThreadPoolManager.teardown.")
        if self._executor:
            self._executor.shutdown()


thread_pool_manager = ThreadPoolManager()


##############################################################################
# Normally this would go into something like endpoints.py
endpoints = Blueprint('v0', __name__, url_prefix='/v0')


def slow_task(i: int, request_id: int) -> int:
    """The slow task."""
    time.sleep(2)
    print(f"Hi from slow_task #{i} in request {request_id} in PID {os.getpid()}")
    return i + 1


def slow_task_callback(j: int) -> None:
    """I do something with result of slow_task."""
    print(f"Hi from slow_task_callback. I got {j}.")


REQUEST_ID = {"counter": 0}

@endpoints.route("/sleepy")
def sleepy() -> dict:
    """Starts a slow async task without blocking request."""
    slow_tasks = 5  # int(request.get_json().get("slow_tasks", 5))
    REQUEST_ID["counter"] += 1
    for i in range(slow_tasks):
        future = thread_pool_manager.executor.submit(slow_task, i, REQUEST_ID["counter"])
        future.add_done_callback(lambda f: slow_task_callback(f.result()))

    time.sleep(1)
    print(f"Hi from sleepy request {REQUEST_ID['counter']} in PID {os.getpid()}")
    return {"status": "ok"}


##############################################################################
# This is all that you'd have in main.py.
def create_app() -> Flask:
    """App factory."""
    app = Flask(__name__)
    app.register_blueprint(endpoints)
    print("registering thread_pool_manager.")
    thread_pool_manager.init_app(app)
    atexit.register(thread_pool_manager.teardown)
    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
