#!/bin/sh
gunicorn --config /usr/src/app/app/gunicorn_config.py main:app