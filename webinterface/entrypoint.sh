#!/bin/sh

echo "Waiting for DBs..."

while ! nc -z $DB_HOST $PG_PORT; do
    echo "DB not read"
    sleep 1
done

echo "DB started"

#python manage.py collectstatic --no-input

python manage.py makemigrations assetscontrol
python manage.py migrate assetscontrol --noinput

python manage.py makemigrations
python manage.py migrate --noinput

if [ $create_superuser = 'yes' ]; then

python manage.py shell -c "import os
from django.contrib.auth import get_user_model
User = get_user_model()
if (not User.objects.filter(username=os.environ.get('SUPERUSER_NAME')).exists()):
    User.objects.create_superuser(os.environ.get('SUPERUSER_NAME'), os.environ.get('SUPERUSER_MAIL'), os.environ.get('SUPERUSER_PASSWORD'))
else:
    pass"
fi

exec python manage.py runserver $WEBINTERFACE_HOST:8000