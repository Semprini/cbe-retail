FROM python:3-alpine

ENV PYTHONUNBUFFERED 1

RUN apk update
RUN apk add py-pip

RUN pip install -U pip
RUN pip install requests pika
ADD *.py /

CMD [ "python", "-u", "./deliver_to_xero.py" ]
