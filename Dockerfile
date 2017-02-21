# Start with a Python image.
FROM python:latest

# Some stuff that everyone has been copy-pasting
# since the dawn of time.
ENV PYTHONUNBUFFERED 1

# Install some necessary things.
RUN apt-get update
RUN apt-get install -y swig libssl-dev dpkg-dev netcat libmysqlclient-dev

# Copy all our files into the image.
#RUN mkdir /code
RUN git clone https://github.com/Semprini/cbe-retail.git /code
WORKDIR /code
#CD /code

# Install our requirements.
RUN pip install -U pip
RUN pip install -Ur requirements.txt
RUN pip install uwsgi mysqlclient

# Collect our static media if serviing via uwsgi.
#RUN python manage.py collectstatic --noinput

# Specify the command to run when the image is run.
RUN ["chmod", "+x", "/code/manage_run.sh"]
RUN ["chmod", "+x", "/code/manage.py"]
CMD ["/code/manage_run.sh"]
