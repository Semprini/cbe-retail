#!/bin/bash

./manage.py migrate
#uwsgi --ini uwsgi.ini
./manage.py runserver 0.0.0.0:8000
