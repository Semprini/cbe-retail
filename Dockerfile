# Start with a Python image.
FROM python:3-alpine

# Set default required environment variables
ENV PYTHONUNBUFFERED 1

ENV DBENGINE sqlite3
ENV DBNAME /code/dblocal.sqlite3
ENV DBHOST None
ENV DBPORT None
ENV DBUSER None
ENV DBPASSWORD None

ENV SUNAME super 
ENV SUEMAIL super@super.com
ENV SUPASS super

ENV MQHOST None
ENV MQUSER None
ENV MQPASSWORD None
ENV MQRESTSERVER '127.0.0.1'
ENV MQRESTPORT 8000

# Install some necessary things.
RUN apt-get update
RUN apt-get install -y swig libssl-dev dpkg-dev netcat libmysqlclient-dev

# Install dependencies not in requirements.txt
RUN pip install -U pip
RUN pip install uwsgi mysqlclient psycopg2

# Copy all our files into the image.
RUN git clone https://github.com/Semprini/cbe-retail.git /code
WORKDIR /code
RUN pip install -Ur requirements.txt

# Collect our static media
RUN python manage.py collectstatic --noinput

# Specify the command to run when the image is run.
RUN ["chmod", "+x", "/code/manage_run.sh"]
#RUN ["chmod", "+x", "/code/manage.py"]
CMD ["/code/manage_run.sh"]
