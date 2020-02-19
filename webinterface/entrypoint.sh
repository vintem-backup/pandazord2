#!/bin/sh

echo "Waiting for DBs..."

while ! nc -z $DB_HOST $PG_PORT; do
    echo "DB not read"
    sleep 1
done

echo "DB started"

#pipenv run python manage.py collectstatic --no-input

pipenv run python manage.py makemigrations controllers
pipenv run python manage.py migrate controllers --noinput

pipenv run python manage.py makemigrations
pipenv run python manage.py migrate --noinput

if [ $create_superuser = 'yes' ]; then

pipenv run python manage.py shell -c "import os
from django.contrib.auth import get_user_model
User = get_user_model()
if (not User.objects.filter(username=os.environ.get('SUPERUSER_NAME')).exists()):
    User.objects.create_superuser(os.environ.get('SUPERUSER_NAME'), os.environ.get('SUPERUSER_MAIL'), os.environ.get('SUPERUSER_PASSWORD'))
else:
    pass"
fi

exec pipenv run python manage.py runserver $WEBINTERFACE:8000