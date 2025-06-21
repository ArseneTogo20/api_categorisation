# API de Catégorisation de Messages Financiers

Ce projet est une API REST développée avec Django et Django REST Framework, conçue pour recevoir, traiter et catégoriser des messages de transactions financières. Elle est entièrement dockerisée pour faciliter le développement et le déploiement.

## Table des Matières
1.  [Technologies](#technologies)
2.  [Fonctionnalités Clés](#fonctionnalités-clés)
3.  [Pour le Développeur Backend](#pour-le-développeur-backend)
    *   [Structure du Projet](#structure-du-projet)
    *   [Installation avec Docker (Recommandé)](#installation-avec-docker-recommandé)
    *   [Commandes Docker Utiles](#commandes-docker-utiles)
    *   [Installation Locale (Alternative)](#installation-locale-alternative)
4.  [Pour le Développeur Frontend](#pour-le-développeur-frontend)
    *   [URL de Base de l'API](#url-de-base-de-lapi)
    *   [Flux d'Authentification JWT](#flux-dauthentification-jwt)
    *   [Documentation des Endpoints](#documentation-des-endpoints)
        *   [Authentification](#authentification-1)
        *   [Gestion des Utilisateurs](#gestion-des-utilisateurs)

---

## Technologies

*   **Backend**: Python 3.11, Django 4.2, Django REST Framework 3.14
*   **Base de Données**: MySQL 8.0
*   **Serveur d'Application**: Gunicorn
*   **Authentification**: JWT (djangorestframework-simplejwt)
*   **Conteneurisation**: Docker & Docker Compose
*   **Documentation API**: Swagger (drf-yasg) & ReDoc

---

## Fonctionnalités Clés

*   ✅ Gestion complète des utilisateurs (CRUD).
*   ✅ Authentification sécurisée par JWT avec système de `refresh token`.
*   ✅ Permissions basées sur les rôles (Utilisateur, Administrateur).
*   ✅ Environnement de développement et de production entièrement dockerisé.
*   ✅ Documentation automatique de l'API via Swagger et ReDoc.
*   *À venir : Endpoint de traitement et de catégorisation des messages.*

---

## Pour le Développeur Backend

Cette section vous guide pour mettre en place l'environnement de développement.

### Structure du Projet

```
.
├── projet_categorisation/  # Configuration principale de Django
├── users/                  # Application pour la gestion des utilisateurs
├── message_processing/     # Application pour la logique métier
├── .env                    # Fichier des variables d'environnement (NE PAS PARTAGER)
├── Dockerfile              # Recette pour construire l'image de l'API
├── docker-compose.yml      # Orchestration des conteneurs (API + DB)
├── entrypoint.sh           # Script de démarrage du conteneur API
├── manage.py               # Utilitaire Django
├── requirements.txt        # Dépendances Python
└── README.md               # Ce fichier
```

### Installation avec Docker (Recommandé)

Assurez-vous que **Docker** et **Docker Compose** sont installés et en cours d'exécution sur votre machine.

1.  **Clonez le projet**
    ```bash
    git clone <url-du-repo>
    cd projet_categorisation
    ```

2.  **Créez le fichier d'environnement**
    Le projet utilise un fichier `.env` pour gérer les secrets. Copiez l'exemple et personnalisez-le si nécessaire.
    ```bash
    # Sur Windows (PowerShell)
    copy .env.example .env

    # Sur Linux/macOS
    cp .env.example .env
    ```
    *Note : J'ai déjà créé le fichier `.env` pour vous, cette étape est pour information.*

3.  **Lancez les conteneurs**
    Cette commande unique va construire l'image de l'API, télécharger l'image MySQL, et démarrer les deux conteneurs en arrière-plan.
    ```bash
    docker-compose up --build -d
    ```

4.  **Créez un superutilisateur**
    La première fois, vous aurez besoin d'un administrateur pour accéder à l'interface d'administration.
    ```bash
    docker-compose exec api python manage.py createsuperuser
    ```
    Suivez les instructions pour créer votre compte.

Votre environnement est prêt !
*   L'API est accessible sur `http://localhost:8000`
*   La base de données tourne sur le port `3307` de votre machine (mappé au port 3306 du conteneur).
*   L'admin Django est sur `http://localhost:8000/admin/`

### Commandes Docker Utiles

*   **Voir les logs en temps réel** :
    ```bash
    docker-compose logs -f
    ```

*   **Exécuter une commande dans le conteneur de l'API** (ex: lancer les migrations) :
    ```bash
    docker-compose exec api <votre-commande>
    # Exemple:
    docker-compose exec api python manage.py makemigrations
    ```

*   **Arrêter les conteneurs** :
    ```bash
    docker-compose down
    ```

*   **Arrêter et supprimer la base de données** (pour repartir de zéro) :
    ```bash
    docker-compose down -v
    ```

### Installation Locale (Alternative)

Si vous ne souhaitez pas utiliser Docker, vous pouvez suivre les étapes traditionnelles :
1.  Assurez-vous d'avoir Python 3.11+ et un serveur MySQL.
2.  Créez et activez un environnement virtuel.
3.  Installez les dépendances : `pip install -r requirements.txt`.
4.  Configurez vos variables d'environnement pour la base de données.
5.  Lancez les migrations : `python manage.py migrate`.
6.  Lancez le serveur de développement : `python manage.py runserver`.

---

## Pour le Développeur Frontend

Cette section explique comment interagir avec l'API.

### URL de Base de l'API

L'URL de base pour toutes les requêtes est : `http://localhost:8000/api/`

### Flux d'Authentification JWT

L'API utilise des `access token` (courte durée) et des `refresh token` (longue durée).

1.  **Inscription/Connexion** : L'utilisateur s'inscrit ou se connecte. Le serveur renvoie un `access_token` et un `refresh_token`.
2.  **Stockage des Tokens** : Stockez le `refresh_token` de manière sécurisée et persistante (ex: `localStorage` ou `HttpOnly cookie`). Stockez l'`access_token` en mémoire.
3.  **Requêtes Authentifiées** : Pour chaque requête vers un endpoint protégé, incluez l'`access_token` dans l'en-tête :
    ```
    Authorization: Bearer <votre_access_token>
    ```
4.  **Gestion de l'Expiration** : Si une requête renvoie une erreur `401 Unauthorized`, cela signifie que l'`access_token` a expiré.
5.  **Rafraîchissement** : Utilisez le `refresh_token` pour appeler l'endpoint `POST /api/token/refresh/`. Vous recevrez un nouvel `access_token`.
6.  **Nouvel Essai** : Réessayez la requête qui avait échoué à l'étape 4 avec le nouvel `access_token`.
7.  **Déconnexion** : Supprimez les tokens du stockage local. Pour plus de sécurité, vous pouvez appeler `POST /api/logout/` pour invalider le `refresh_token` côté serveur.

### Documentation des Endpoints

Voici les endpoints principaux. Pour une documentation interactive complète, visitez :
*   **Swagger UI**: `http://localhost:8000/swagger/`
*   **ReDoc**: `http://localhost:8000/redoc/`

---

#### Authentification

##### `POST /api/register/`
Crée un nouvel utilisateur.
*   **Authentification**: Aucune requise.
*   **Request Body**:
    ```json
    {
        "nom": "Dupont",
        "prenom": "Jean",
        "numero_de_telephone": "90112233",
        "email": "jean.dupont@email.com",
        "password": "votreMotDePasseSolide123!",
        "password_confirm": "votreMotDePasseSolide123!"
    }
    ```
*   **Success Response (201 CREATED)**:
    ```json
    {
        "message": "Utilisateur créé avec succès",
        "user": { "user_id": "...", "nom": "Dupont", ... },
        "tokens": {
            "access": "eyJ...",
            "refresh": "eyJ..."
        }
    }
    ```

##### `POST /api/login/`
Connecte un utilisateur et renvoie les tokens.
*   **Authentification**: Aucune requise.
*   **Request Body**:
    ```json
    {
        "numero_de_telephone": "90112233",
        "password": "votreMotDePasseSolide123!"
    }
    ```
*   **Success Response (200 OK)**:
    ```json
    {
        "message": "Connexion réussie",
        "user": { ... },
        "tokens": {
            "access": "eyJ...",
            "refresh": "eyJ..."
        }
    }
    ```

##### `POST /api/token/refresh/`
Renvoie un nouvel `access_token` valide.
*   **Authentification**: Aucune requise.
*   **Request Body**:
    ```json
    {
        "refresh": "<votre_refresh_token>"
    }
    ```
*   **Success Response (200 OK)**:
    ```json
    {
        "access": "eyJ...",
        "refresh": "eyJ..." // Un nouveau refresh token est aussi renvoyé
    }
    ```

##### `POST /api/logout/`
Invalide (blacklist) un `refresh_token` pour déconnecter l'utilisateur de manière sécurisée.
*   **Authentification**: Requise (`Bearer <access_token>`).
*   **Request Body**:
    ```json
    {
        "refresh": "<votre_refresh_token>"
    }
    ```
*   **Success Response (200 OK)**:
    ```json
    { "message": "Déconnexion réussie" }
    ```

---

#### Gestion des Utilisateurs

##### `GET /api/users/`
Récupère la liste de tous les utilisateurs.
*   **Authentification**: Requise. **Rôle `admin` uniquement.**
*   **Success Response (200 OK)**:
    ```json
    [
        { "user_id": "...", "nom": "Admin", "role": "admin", ... },
        { "user_id": "...", "nom": "Dupont", "role": "utilisateur", ... }
    ]
    ```

##### `GET /api/profile/`
Récupère les informations du profil de l'utilisateur actuellement connecté.
*   **Authentification**: Requise (`Bearer <access_token>`).
*   **Success Response (200 OK)**:
    ```json
    {
        "user_id": "...",
        "nom": "Dupont",
        ...
    }
    ```

##### `PUT /api/profile/`
Met à jour le profil de l'utilisateur actuellement connecté.
*   **Authentification**: Requise (`Bearer <access_token>`).
*   **Request Body** (envoyez seulement les champs à modifier):
    ```json
    {
        "nom": "Durand",
        "email": "jean.durand@email.com"
    }
    ```
*   **Success Response (200 OK)**:
    ```json
    {
        "message": "Profil mis à jour avec succès",
        "user": { "user_id": "...", "nom": "Durand", ... }
    }
    ``` 