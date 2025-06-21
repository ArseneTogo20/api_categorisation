# Documentation Complète de l'API de Catégorisation

Bienvenue dans la documentation du projet d'API de Catégorisation. Ce document a pour but de guider les développeurs (backend et frontend) pour comprendre, installer, et utiliser ce projet.

## 1. Vue d'ensemble du Projet

Ce projet est une API REST développée avec Django et Django REST Framework. Son objectif principal est de fournir une plateforme pour traiter et catégoriser des messages financiers. Elle est conçue pour être robuste, sécurisée et scalable, en utilisant Docker pour la conteneurisation.

### Technologies Principales
- **Backend**: Python, Django, Django REST Framework
- **Base de données**: MySQL
- **Serveur d'application**: Gunicorn
- **Authentification**: JWT (JSON Web Tokens) avec `djangorestframework-simplejwt`
- **Conteneurisation**: Docker & Docker Compose
- **Documentation d'API**: Swagger & ReDoc (via `drf-yasg`)

## 2. Structure du Projet

Le projet est organisé en plusieurs applications Django, chacune ayant un rôle spécifique :

```
.
├── message_processing/  # App Django pour la logique de traitement des messages (à développer)
├── projet_categorisation/ # Fichiers de configuration du projet principal (settings.py, urls.py)
├── users/               # App Django pour la gestion des utilisateurs et de l'authentification
├── venv/                  # Environnement virtuel Python (ignoré par git)
├── .env                 # Fichier pour les variables d'environnement (secrets)
├── docker-compose.yml   # Fichier de configuration pour lancer les services avec Docker
├── Dockerfile           # Fichier pour construire l'image Docker de l'application Django
├── entrypoint.sh        # Script exécuté au démarrage du conteneur de l'API
├── manage.py            # Utilitaire de ligne de commande de Django
├── requirements.txt     # Dépendances Python du projet
└── README.md            # Fichier d'introduction au projet
```

- **`users`**: Cette application gère tout ce qui concerne les utilisateurs : le modèle `CustomUser`, l'inscription, la connexion, la gestion de profil et les permissions.
- **`message_processing`**: C'est le cœur de l'application. Elle contiendra la logique métier pour la catégorisation des messages. Actuellement, elle est vide et prête à être développée.
- **`projet_categorisation`**: C'est le module de configuration principal du projet Django.

## 3. Installation et Lancement (Développement Local)

Le projet est entièrement conteneurisé avec Docker, ce qui simplifie grandement l'installation.

### Prérequis
- [Docker](https://www.docker.com/get-started)
- [Docker Compose](https://docs.docker.com/compose/install/) (généralement inclus avec Docker Desktop)

### Étapes d'installation

**Étape 1 : Cloner le projet**
```bash
git clone <URL_DU_REPOSITORY>
cd <NOM_DU_DOSSIER>
```

**Étape 2 : Configurer les variables d'environnement**
Le projet utilise un fichier `.env` pour gérer les secrets et les configurations. Copiez le fichier d'exemple s'il existe, ou créez un fichier nommé `.env` à la racine du projet et remplissez-le. Il doit contenir au minimum :

```ini
# Django
SECRET_KEY=votre-super-secret-key-a-generer-et-garder-secret
DEBUG=True

# Database
DB_HOST=db
DB_NAME=projet_categorisation
DB_USER=user_app
DB_PASSWORD=password_app
DB_ROOT_PASSWORD=root_password_123
DB_PORT=3306
```
**Important**: La valeur `DB_HOST` doit être `db`, qui est le nom du service de base de données dans `docker-compose.yml`.

**Étape 3 : Construire et Lancer les conteneurs**
Ouvrez un terminal à la racine du projet et lancez la commande suivante :

```bash
docker-compose up --build -d
```
- `--build`: Force la reconstruction des images Docker. C'est nécessaire la première fois ou si vous modifiez le `Dockerfile` ou `requirements.txt`.
- `-d`: Lance les conteneurs en arrière-plan (detached mode).

Les conteneurs de l'API (`projet_api`) et de la base de données (`projet_db`) devraient maintenant être en cours d'exécution. Vous pouvez le vérifier avec `docker ps`.

**Étape 4 : Créer un super-utilisateur (Admin)**
Pour accéder aux parties de l'API réservées aux administrateurs, vous devez créer un compte admin.

```bash
docker exec -it projet_api python manage.py createsuperuser
```
Suivez les instructions pour définir le numéro de téléphone, le nom, l'email et le mot de passe de votre administrateur.

**Félicitations !** Votre environnement de développement est prêt. L'API est accessible à l'adresse `http://127.0.0.1:8000`.

### Commandes utiles de Docker

- **Arrêter les conteneurs**: `docker-compose down`
- **Voir les logs**: `docker-compose logs` ou `docker-compose logs -f api` pour suivre les logs de l'API.
- **Exécuter une commande manage.py**: `docker exec -it projet_api python manage.py <commande>` (ex: `migrate`, `shell`, etc.)

## 4. Documentation de l'API (Endpoints)

L'API est accessible via le préfixe `/api/`. L'authentification se fait via un token JWT (Bearer Token) à fournir dans le header `Authorization`.

`Authorization: Bearer <votre_access_token>`

---
### 4.1. Endpoints d'Authentification (`/api/auth/...`)

Ces endpoints sont ouverts et ne nécessitent pas de token.

#### **Login**
- **URL**: `/api/auth/login/`
- **Méthode**: `POST`
- **Description**: Connecte un utilisateur et retourne ses informations ainsi que des tokens d'accès et de rafraîchissement.
- **Corps de la requête (JSON)**:
  ```json
  {
      "numero_de_telephone": "99595766",
      "password": "votre_mot_de_passe"
  }
  ```
- **Réponse en cas de succès (200 OK)**:
  ```json
  {
      "message": "Connexion réussie",
      "user": {
          "user_id": "uuid-de-l-utilisateur",
          "nom": "ATTIKPO",
          "prenom": "kodjo arsene",
          "numero_de_telephone": "+22898454209",
          "email": "oklukoffistan@gmail.com",
          "role": "admin",
          "date_creation": "...",
          "date_modification": "...",
          "is_active": true
      },
      "tokens": {
          "access": "ey...",
          "refresh": "ey..."
      }
  }
  ```

#### **Refresh Token**
- **URL**: `/api/auth/token/refresh/`
- **Méthode**: `POST`
- **Description**: Permet d'obtenir un nouveau token d'accès en utilisant un token de rafraîchissement valide.
- **Corps de la requête (JSON)**:
  ```json
  {
      "refresh": "votre_refresh_token"
  }
  ```
- **Réponse en cas de succès (200 OK)**:
  ```json
  {
      "access": "nouveau_access_token"
  }
  ```

#### **Logout**
- **URL**: `/api/auth/logout/`
- **Méthode**: `POST`
- **Description**: Déconnecte l'utilisateur en ajoutant son token de rafraîchissement à une liste noire.
- **Corps de la requête (JSON)**:
  ```json
  {
      "refresh_token": "votre_refresh_token"
  }
  ```
- **Réponse en cas de succès (200 OK)**:
  ```json
  {
      "message": "Déconnexion réussie"
  }
  ```

---
### 4.2. Endpoints du Profil Utilisateur (`/api/me/...`)

Ces endpoints nécessitent un token d'authentification valide.

#### **Gérer son profil**
- **URL**: `/api/me/profile/`
- **Méthodes**: `GET`, `PUT`
- **Description**:
    - `GET`: Récupère les informations du profil de l'utilisateur actuellement connecté.
    - `PUT`: Met à jour les informations du profil (nom, prénom, email).
- **Corps de la requête (PUT)**:
  ```json
  {
      "nom": "NouveauNom",
      "prenom": "NouveauPrenom",
      "email": "nouveau@email.com"
  }
  ```
- **Réponse en cas de succès (GET ou PUT)**:
  ```json
  {
      "user_id": "...",
      "nom": "...",
      // ... autres champs utilisateur ...
  }
  ```

#### **Changer son mot de passe**
- **URL**: `/api/me/change-password/`
- **Méthode**: `POST`
- **Description**: Permet à l'utilisateur connecté de changer son mot de passe.
- **Corps de la requête (JSON)**:
  ```json
  {
      "old_password": "ancien_mot_de_passe",
      "new_password": "nouveau_mot_de_passe",
      "new_password_confirm": "nouveau_mot_de_passe"
  }
  ```
- **Réponse en cas de succès (200 OK)**:
  ```json
  {
      "message": "Mot de passe modifié avec succès"
  }
  ```

---
### 4.3. Endpoints de Gestion (Admin) (`/api/admin/...`)

Ces endpoints sont **réservés aux administrateurs** (`role='admin'`). Un token d'un utilisateur admin est requis.

#### **Créer un utilisateur**
- **URL**: `/api/admin/create-user/`
- **Méthode**: `POST`
- **Description**: Crée un nouvel utilisateur. Le rôle est 'utilisateur' par défaut.
- **Corps de la requête (JSON)**:
  ```json
  {
      "nom": "Jean",
      "prenom": "Dupont",
      "numero_de_telephone": "91234567",
      "email": "jean.dupont@example.com",
      "password": "unmotdepassesecurise",
      "password_confirm": "unmotdepassesecurise"
  }
  ```
- **Réponse en cas de succès (201 CREATED)**:
  ```json
  {
      "message": "Utilisateur créé avec succès par un administrateur.",
      "user": {
          // ... détails de l'utilisateur créé ...
      }
  }
  ```

#### **Lister tous les utilisateurs**
- **URL**: `/api/admin/get-all-users/`
- **Méthode**: `GET`
- **Description**: Retourne une liste paginée de tous les utilisateurs du système.
- **Réponse en cas de succès (200 OK)**:
  ```json
  {
      "count": 5,
      "next": "http://.../?page=2",
      "previous": null,
      "results": [
          {
              "user_id": "...",
              // ... autres détails utilisateur ...
          },
          // ... autres utilisateurs ...
      ]
  }
  ```

#### **Gérer un utilisateur spécifique**
- **URL**: `/api/admin/user-details/<uuid:pk>/`
- **Méthodes**: `GET`, `PUT`, `DELETE`
- **Description**:
    - `GET`: Récupère les détails d'un utilisateur spécifique par son UUID.
    - `PUT`: Met à jour les informations d'un utilisateur spécifique.
    - `DELETE`: Ne supprime pas l'utilisateur, mais le désactive (`is_active=False`).
- **Corps de la requête (PUT)**: Permet de modifier le rôle, par exemple.
  ```json
  {
      "role": "admin" // ou "utilisateur"
  }
  ```
- **Réponse en cas de succès (DELETE, 200 OK)**:
  ```json
  {
      "message": "Compte désactivé avec succès"
  }
  ``` 