#!/bin/sh
source .venv/bin/activate
py mysite/manage.py makemigrations
py mysite/manage.py migrate
python mysite/manage.py runserver $PORT
