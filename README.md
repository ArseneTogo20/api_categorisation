# API de Catégorisation de Messages Financiers

Ce projet est une API REST développée avec Django et Django REST Framework, conçue pour traiter et catégoriser des messages financiers. L'ensemble du projet est conteneurisé avec Docker pour faciliter le développement et le déploiement.

[![Python](https://img.shields.io/badge/Python-3.11-blue.svg)](https://www.python.org/downloads/release/python-311/)
[![Django](https://img.shields.io/badge/Django-4.2-darkgreen.svg)](https://www.djangoproject.com/)
[![Docker](https://img.shields.io/badge/Docker-blue.svg)](https://www.docker.com/)

## Fonctionnalités
- **Gestion complète des utilisateurs** : Authentification JWT, inscription, gestion de profil.
- **Permissions basées sur les rôles** : Distinction entre les utilisateurs normaux et les administrateurs.
- **API RESTful** : Endpoints clairs et structurés.
- **Environnement Dockerisé** : Installation et déploiement simplifiés.
- **Prêt pour le développement** : L'application `message_processing` est prête à accueillir la logique métier.

## Démarrage Rapide (Quick Start)

Suivez ces étapes pour lancer le projet en local.

### Prérequis
- [Docker](https://www.docker.com/get-started) & [Docker Compose](https://docs.docker.com/compose/install/)

### Installation
1. **Clonez ce dépôt**
   ```bash
   git clone <URL_DU_REPOSITORY>
   cd <NOM_DU_DOSSIER>
   ```

2. **Créez le fichier d'environnement**
   Créez un fichier `.env` à la racine du projet et remplissez-le en vous basant sur cet exemple :
   ```ini
   SECRET_KEY=votre-secret-key
   DEBUG=True
   DB_HOST=db
   DB_NAME=projet_categorisation
   DB_USER=user_app
   DB_PASSWORD=password_app
   DB_ROOT_PASSWORD=root_password_123
   DB_PORT=3306
   ```

3. **Lancez les conteneurs**
   ```bash
   docker-compose up --build -d
   ```

4. **Créez un compte administrateur**
   ```bash
   docker exec -it projet_api python manage.py createsuperuser
   ```
   Suivez les instructions pour créer votre premier utilisateur.

Votre API est maintenant accessible sur `http://127.0.0.1:8000`.

## Documentation

- La documentation complète du projet, incluant le détail de chaque endpoint de l'API, est disponible dans le fichier [`DOCUMENTATION.md`](./DOCUMENTATION.md).
- Une fois l'application lancée, la documentation Swagger est également accessible sur `http://127.0.0.1:8000/swagger/` et ReDoc sur `http://127.0.0.1:8000/redoc/`.

## Prochaines Étapes
Le développement de la logique métier principale doit se faire dans l'application `message_processing`.
- Définir les modèles dans `message_processing/models.py`.
- Créer les sérialiseurs et les vues correspondantes.
- Ajouter les nouvelles URL dans `message_processing/urls.py`.
