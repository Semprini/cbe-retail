FROM python:3
RUN pip install requests pika
ADD calculate_shareable_margin.py /
CMD [ "python", "-u", "./calculate_shareable_margin.py" ]
