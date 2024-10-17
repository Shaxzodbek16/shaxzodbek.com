#!/bin/bash

sleep 2

python manage.py makemigrations

sleep 2

python manage.py migrate

sleep 2

python manage.py runserver
