#!/bin/sh

set -e

# Simple wait script
echo 'Waiting for database to be ready...'
while ! python -c 'import MySQLdb; MySQLdb.connect(host=\"db\", user=\"devuser\", password=\"changeme\", database=\"devdb\")' 2>/dev/null; do
  echo 'Database not ready yet, waiting...'
  sleep 1
done
echo 'Database is ready!'
python manage.py collectstatic --noinput
python manage.py migrate

uwsgi --socket :9000 --worker 4 --master --enable-threads --module app.wsgi