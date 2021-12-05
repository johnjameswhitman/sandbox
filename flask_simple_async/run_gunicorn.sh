#!/usr/bin/env bash

gunicorn --workers 4 --bind :5000 --worker-class gthread "main:create_app()"
