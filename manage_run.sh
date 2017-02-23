#!/bin/bash
# Create local_settings.py from environment variables
echo -e "import os\n\
from retail.settings import BASE_DIR\n\n\
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))\n\
DATABASES = {\n\
    'default': {\n\
        'ENGINE': 'django.db.backends.${DBENGINE}',\n\
        'NAME': '${DBNAME}',\n\
        'HOST': '${DBHOST}',\n\
        'PORT': ${DBPORT},\n\
        'USER': '${DBUSER}',\n\
        'PASSWORD': '${DBPASSWORD}',\n\
    }\n\
}\n" > /code/retail/local_settings.py

#python manage.py makemigrations business_interaction customer location trouble physical_object supplier_partner resource human_resources product pricing sale
python manage.py migrate --run-syncdb
#uwsgi --ini uwsgi.ini
python manage.py runserver 0.0.0.0:8000
