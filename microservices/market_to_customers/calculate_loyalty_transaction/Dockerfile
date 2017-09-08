FROM python:3-alpine

ENV PYTHONUNBUFFERED 1
ENV QUEUE_HOST cbeq
ENV QUEUE_USER super
ENV QUEUE_PASS super

ENV API_HOST cbeq
ENV API_USER super
ENV API_PASS super

RUN apk update
RUN apk add py-pip

RUN pip install -U pip

ADD *.py /
ADD requirements.txt
RUN pip install -Ur requirements.txt


CMD [ "python", "-u", "./calculate_loyalty_transaction.py" ]

