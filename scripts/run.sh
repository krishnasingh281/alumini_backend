#!/bin/sh
set -e

# Wait for database
./wait-for-db.sh

# Run migrations and collect static files
python manage.py collectstatic --noinput
python manage.py migrate

# Start the application
uwsgi --socket :9000 --workers 4 --master --enable-threads --module app.wsgi