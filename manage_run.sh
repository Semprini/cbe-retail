#!/bin/bash

python manage.py migrate
#uwsgi --ini uwsgi.ini
python manage.py runserver 0.0.0.0:8000
