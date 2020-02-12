#!/bin/sh

echo "Waiting for DBs..."

while ! nc -z $DB_HOST $PG_PORT; do
    echo "DB not read"
    sleep 1
done

echo "DB started"

exec pipenv run python listening_of_binance_assets_table.py