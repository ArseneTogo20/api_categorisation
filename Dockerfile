# 1. Base Image
# Utiliser une image Python officielle comme image de base
FROM python:3.11-slim

# 2. Environment Variables
# Empêche Python de créer des fichiers .pyc et de mettre les sorties en mémoire tampon
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# 3. Work Directory
# Définir le répertoire de travail dans le conteneur
WORKDIR /app

# 4. Install Dependencies
# Installer les dépendances système nécessaires, y compris netcat pour le script d'entrypoint
RUN apt-get update && apt-get install -y build-essential pkg-config default-libmysqlclient-dev netcat-openbsd && rm -rf /var/lib/apt/lists/*

# Copier et installer les dépendances avant de copier le reste du code pour profiter du cache de Docker
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy Project Code
# Copier le code du projet dans le répertoire de travail
COPY . .

# Copier et donner les permissions au script d'entrypoint
COPY ./entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

# 6. Collect Static Files (pour la production)
RUN python manage.py collectstatic --noinput

# 7. Expose Port
# Exposer le port sur lequel Gunicorn va tourner
EXPOSE 8000

# 8. Run Command
# Lancer le script d'entrypoint. Ce script va ensuite lancer le serveur.
ENTRYPOINT ["/app/entrypoint.sh"] 