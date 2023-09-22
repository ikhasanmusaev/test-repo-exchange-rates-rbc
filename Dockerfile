FROM python:3.10

ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY ./requirements.txt /app/

RUN pip install -r requirements.txt

#Install Cron
RUN apt-get update
RUN apt-get -y install cron

COPY . /app/

#COPY ./docker-entrypoint.sh /
#RUN chmod +x /docker-entrypoint.sh

#ENTRYPOINT ["/docker-entrypoint.sh"]


#RUN python manage.py migrate
#RUN python manage.py crontab add
