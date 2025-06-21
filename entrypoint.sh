#!/bin/sh

# On lance les migrations
echo "Running migrations..."
python manage.py migrate

# On démarre le serveur avec Gunicorn
echo "Starting server with Gunicorn..."
exec gunicorn projet_categorisation.wsgi:application --bind 0.0.0.0:8000 --workers 3 