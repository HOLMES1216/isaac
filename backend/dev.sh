#!/bin/bash
source my_project_env/Scripts/activate

python manage.py makemigrations
python manage.py migrate
python manage.py init
daphne -b 0.0.0.0 -p 8000 application.asgi:application
