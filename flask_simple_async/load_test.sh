#!/usr/bin/env bash

ab -n 200 -c 100 http://localhost:5000/v0/sleepy
