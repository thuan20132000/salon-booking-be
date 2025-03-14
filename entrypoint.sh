#!/bin/sh

if [ "$DB_HOSTNAME" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $DB_HOSTNAME $DB_PORT; do
        sleep 0.1
    done

    echo "PostgreSQL started"
fi

python manage.py migrate

exec "$@"