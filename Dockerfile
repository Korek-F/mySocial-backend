FROM python:3.8-slim-buster

ENV PYTHONUNBUFFERED 1 

RUN pip install --upgrade pip   

WORKDIR /code

COPY ./requirements.txt . 
RUN pip install -r requirements.txt 
RUN pip install channels
RUN pip install channels-redis
RUN pip install gunicorn
RUN pip install psycopg2-binary
RUN pip install daphne

COPY . .

