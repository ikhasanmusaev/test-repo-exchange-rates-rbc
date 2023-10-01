FROM python:3.10

ENV PYTHONUNBUFFERED 1
do
WORKDIR /app

COPY ./requirements.txt /app/

RUN pip install -r requirements.txt

#Install Cron
RUN apt-get update

COPY . /app/
