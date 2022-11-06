# T>/PE
## Table of contents
* [General info](#general-info)
* [Technologies](#technologies)
* [Setup](#setup)

## General info
This app is a backend api for T>/PE app. 

## Technologies
* Django
* Rest Framework
* Django Channels
* Docker
* Nginx

## Setup
* add .env file in main directory
* edit .env:
  add SECRET_KEY = "{your secret key to app}" 
  add EMAIL_HOST_USER = "{your google bot email address}" 
  add EMAIL_HOST_PASSWORD = "{your google bot email password}" 
* run your docker program
* open terminal in main directory 
* runc docker-compose file: docker-compose up --build 
* setup project, run: 
  - docker-compose run django_gunicorn python manage.py collectstatic
  - docker-compose run django_gunicorn python manage.py makemigrations
  - docker-compose run django_gunicorn python manage.py migrate
* check if it works, go to http://localhost/auth/registration/
