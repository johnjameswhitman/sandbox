#!/usr/bin/env bash

gunicorn --workers 4 --worker-class gevent --bind :5000 "main:create_app()"
