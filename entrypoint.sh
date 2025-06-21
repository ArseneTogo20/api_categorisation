#!/bin/sh

# On attend que la base de données soit prête
echo "Waiting for database..."
while ! nc -z $DB_HOST $DB_PORT; do
  sleep 0.1
done
echo "Database started"

# On lance les migrations
echo "Running migrations..."
python manage.py migrate

# On démarre le serveur
echo "Starting server..."
python manage.py runserver 0.0.0.0:8000

exec "$@" 