#!/usr/bin/env sh

# python manage.py makemigrations --no-input
# python manage.py migrate --no-input
python manage.py collectstatic --no-input
# python manage.py createsuperuser --noinput --username svyat --email sursvyat@gmail.com

gunicorn rusanitapp.wsgi:application --bind 0.0.0.0:8000 --reload -w 4
