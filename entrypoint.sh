#!/bin/sh
#gunicorn --config gunicorn_config.py app:app
export FLASK_ENV=development
source env/bin/activate 
python app.py
