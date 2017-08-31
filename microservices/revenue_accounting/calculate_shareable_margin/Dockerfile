FROM python:3-alpine

ENV PYTHONUNBUFFERED 1

RUN apk update
RUN apk add py-pip

RUN pip install requests pika
ADD calculate_shareable_margin.py /

CMD [ "python", "-u", "./calculate_shareable_margin.py" ]
