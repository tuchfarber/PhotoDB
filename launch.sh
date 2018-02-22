#!/bin/bash
cd PhotoDB
python ./manage.py migrate
python ./manage.py create_super_user --username $DJANGO_USERNAME --password $DJANGO_PASSWORD --noinput --email 'abc@example.com'
python ./manage.py collectstatic --clear
gunicorn -b 0.0.0.0:80 photodb.wsgi