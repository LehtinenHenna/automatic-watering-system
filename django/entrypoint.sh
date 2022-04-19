#!/bin/bash

if [ "$DJANGO_SUPERUSER_USERNAME" ]
then
  python manage.py createsuperuser \
    --no-input \
    --username $DJANGO_SUPERUSER_USERNAME \
    --email $DJANGO_SUPERUSER_EMAIL
fi

gunicorn water_world_server.wsgi:application --bind 0.0.0.0:8000
