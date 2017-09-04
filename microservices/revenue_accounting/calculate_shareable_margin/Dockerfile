FROM python:3-alpine

ENV PYTHONUNBUFFERED 1
ENV QUEUE_HOST cbeq
ENV QUEUE_USER super
ENV QUEUE_PASS super

RUN apk update
RUN apk add py-pip

RUN pip install -U pip
RUN pip install requests pika
ADD *.py /

CMD [ "python", "-u", "./calculate_shareable_margin.py" ]
