#!/usr/bin/env bash

ab -n 400 -c 20 http://localhost:5000/v0/sleepy
