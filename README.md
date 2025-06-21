# API de Catégorisation de Messages Financiers

Une API RESTful développée avec Django et entièrement conteneurisée avec Docker. Elle fournit une base solide pour la gestion des utilisateurs, l'authentification JWT, et la catégorisation de messages financiers.

---

## 🚀 Démarrage Rapide (avec Docker)

Le moyen le plus simple et le plus rapide de lancer le projet. Assurez-vous que **Docker Desktop** est en cours d'exécution.

1.  **Clonez le projet**
    ```bash
    git clone <url-du-repo>
    cd projet_categorisation
    ```

2.  **Lancez les conteneurs**
    Cette commande unique construit et démarre l'API et la base de données.
    ```bash
    docker-compose up --build -d
    ```
    *(Le `-d` signifie "detached", pour le lancer en arrière-plan).*

3.  **Créez un superutilisateur**
    La première fois, créez un compte administrateur pour accéder à tout.
    ```bash
    docker-compose exec api python manage.py createsuperuser
    ```

**C'est tout !** Votre environnement est maintenant opérationnel :
*   **API disponible sur** : `http://localhost:8000/api/`
*   **Documentation interactive (Swagger)** : `http://localhost:8000/swagger/`
*   **Interface d'administration** : `http://localhost:8000/admin/`

---

## 📖 Guide pour Développeur Frontend

Cette section contient tout ce dont vous avez besoin pour interagir avec l'API.

### URL de Base
Toutes les requêtes d'API doivent être préfixées par :
`http://localhost:8000/api`

### Flux d'Authentification JWT

L'API utilise un système de jetons JWT standard.

1.  **Obtenez les Tokens** : Lors de l'inscription (`/register`) ou de la connexion (`/login`), le serveur vous renvoie un `access_token` (durée de vie : 60 min) et un `refresh_token` (durée de vie : 24h).

2.  **Stockez les Tokens** :
    *   Stockez l'`access_token` en mémoire (ex: dans une variable d'état de votre application).
    *   Stockez le `refresh_token` de manière persistante et sécurisée (ex: dans un cookie `HttpOnly` ou le `localStorage`).

3.  **Effectuez des Requêtes Authentifiées** : Pour tous les endpoints protégés, ajoutez l'en-tête `Authorization`.
    ```
    Authorization: Bearer <votre_access_token>
    ```

4.  **Gérez l'Expiration** : Si une requête renvoie une erreur `401 Unauthorized`, l'`access_token` a expiré. Vous devez alors :
    a. Appeler l'endpoint `POST /token/refresh/` en envoyant votre `refresh_token` dans le corps de la requête.
    b. Vous recevrez en retour un nouvel `access_token`.
    c. Mettez à jour l'`access_token` que vous avez en mémoire et relancez la requête qui avait échoué.

### Endpoints de l'API

> Pour tester et voir tous les détails, utilisez la [documentation Swagger](http://localhost:8000/swagger/).

#### **Authentification**

`POST /register/`
*   **Description**: Crée un nouvel utilisateur.
*   **Body**:
    ```json
    {
        "nom": "Dupont", "prenom": "Jean",
        "numero_de_telephone": "90112233",
        "email": "jean.dupont@email.com",
        "password": "MotDePasseSolide123!",
        "password_confirm": "MotDePasseSolide123!"
    }
    ```

`POST /login/`
*   **Description**: Connecte un utilisateur existant.
*   **Body**:
    ```json
    {
        "numero_de_telephone": "90112233",
        "password": "MotDePasseSolide123!"
    }
    ```

`POST /token/refresh/`
*   **Description**: Rafraîchit un `access_token` expiré.
*   **Body**:
    ```json
    { "refresh": "<votre_refresh_token>" }
    ```

#### **Utilisateurs**

`GET /profile/`
*   **Description**: Récupère les informations du profil de l'utilisateur connecté.
*   **Auth**: Requise (Bearer Token).

`PUT /profile/`
*   **Description**: Met à jour le profil de l'utilisateur connecté.
*   **Auth**: Requise (Bearer Token).
*   **Body**: `{ "nom": "NouveauNom", "email": "nouvel@email.com" }` (envoyez seulement les champs à modifier).

`GET /users/`
*   **Description**: Récupère la liste de tous les utilisateurs.
*   **Auth**: Requise. **Rôle `admin` uniquement.**

---

## 🛠️ Guide pour Développeur Backend

Détails pour ceux qui souhaitent modifier ou étendre le code source.

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

### Commandes Docker Utiles

*   **Voir les logs en temps réel** :
    `docker-compose logs -f`

*   **Lancer une commande Django** (ex: créer des migrations) :
    `docker-compose exec api python manage.py makemigrations`

*   **Ouvrir un shell dans le conteneur** :
    `docker-compose exec api /bin/sh`

*   **Arrêter les conteneurs** :
    `docker-compose down`

*   **Forcer une reconstruction de l'image** :
    `docker-compose up --build -d`

*   **Tout supprimer (conteneurs ET base de données)** :
    `docker-compose down -v`

### Installation sans Docker (Alternative)

1.  Assurez-vous d'avoir Python 3.11+ et un serveur MySQL.
2.  Créez un environnement virtuel (`python -m venv venv` et `source venv/bin/activate`).
3.  Installez les dépendances : `pip install -r requirements.txt`.
4.  Configurez un fichier `.env` avec les accès à votre base de données locale (`DB_HOST=localhost`).
5.  Lancez les migrations : `python manage.py migrate`.
6.  Lancez le serveur : `python manage.py runserver`.
