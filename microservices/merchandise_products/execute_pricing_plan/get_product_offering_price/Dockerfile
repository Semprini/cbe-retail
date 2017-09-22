FROM python:3-alpine

ENV PYTHONUNBUFFERED 1

ENV API_USER super
ENV API_PASS super
ENV FLASK_APP=get_product_offering_price.py

RUN apk update
RUN apk add py-pip
RUN apk add git

RUN pip install -U pip

ADD *.py /
ADD requirements.txt /
RUN pip install -Ur /requirements.txt

CMD [ "python", "-m", "flask", "run" ]
