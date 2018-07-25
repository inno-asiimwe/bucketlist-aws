#!/bin/sh

echo "waiting for postgres"

while ! netcat -z database 5432; do
    sleep 0.1
done

echo "postgres started"
python manage.py db init

python manage.py db migrate

python manage.py db upgrade

python run.py