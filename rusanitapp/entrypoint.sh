#!/usr/bin/env sh

python manage.py makemigrations
python manage.py migrate

gunicorn rusanitapp.wsgi:application --bind 0.0.0.0:8000 --reload -w 4
