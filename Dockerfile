# Start with a Python image.
FROM python:latest

# Some stuff that everyone has been copy-pasting
# since the dawn of time.
ENV PYTHONUNBUFFERED 1

# Install some necessary things.
RUN apt-get update
RUN apt-get install -y swig libssl-dev dpkg-dev netcat libmysqlclient-dev

# Copy all our files into the image.
RUN mkdir /code
WORKDIR /code
COPY . /code/

# Install our requirements.
RUN pip install -U pip
RUN pip install -Ur requirements.txt
RUN pip install uwsgi mysqlclient

# Collect our static media.
RUN /code/manage.py collectstatic --noinput

# Specify the command to run when the image is run.
CMD ["/code/manage_run.sh"]
