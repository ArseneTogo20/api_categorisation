#!/bin/sh

# On lance les migrations
echo "Running migrations..."
python manage.py migrate

# Si une commande est passée en paramètre, on l'exécute
if [ $# -gt 0 ]; then
    echo "Executing command: $@"
    exec "$@"
else
    # Sinon, on démarre le serveur avec Gunicorn (comportement par défaut)
    echo "Starting server with Gunicorn..."
    exec gunicorn projet_categorisation.wsgi:application --bind 0.0.0.0:8000 --workers 3
fi 