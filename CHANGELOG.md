# Changelog

Tous les changements notables de ce projet seront documentés dans ce fichier.

Le format est basé sur [Keep a Changelog](https://keepachangelog.com/fr/1.0.0/),
et ce projet adhère au [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-06-28

### Ajouté
- API Django REST complète pour la catégorisation de messages
- Authentification JWT avec gestion des utilisateurs personnalisée
- Système de traitement asynchrone avec Celery et Redis
- Enregistrement de messages en masse avec détection de doublons
- Catégorisation automatique des messages SMS/transactions
- API pour récupérer les messages traités avec pagination
- Conteneurisation complète avec Docker et Docker Compose
- Base de données MySQL pour la persistance des données
- Documentation complète avec README détaillé

### Fonctionnalités principales
- **Authentification** : Connexion sécurisée par JWT
- **Gestion des utilisateurs** : Modèle CustomUser avec numéro de téléphone
- **Enregistrement de messages** : Endpoint optimisé pour le volume
- **Traitement asynchrone** : Worker Celery pour la catégorisation
- **API REST** : Endpoints complets pour toutes les opérations
- **Docker** : Environnement de développement et production

### Technologies utilisées
- Django 4.2 + Django REST Framework
- Celery pour le traitement asynchrone
- Redis comme broker de tâches
- MySQL 8.0 pour la base de données
- Docker et Docker Compose
- JWT pour l'authentification

### Configuration
- Support des variables d'environnement
- Configuration Celery optimisée
- Sécurité renforcée avec validation des données
- Gestion des permissions par rôle

## [0.1.0] - 2025-06-28

### Ajouté
- Structure initiale du projet Django
- Configuration de base avec Docker
- Modèles de données pour les utilisateurs et messages
- API REST basique

---

## Types de changements

- **Ajouté** pour les nouvelles fonctionnalités
- **Modifié** pour les changements dans les fonctionnalités existantes
- **Déprécié** pour les fonctionnalités qui seront bientôt supprimées
- **Supprimé** pour les fonctionnalités supprimées
- **Corrigé** pour les corrections de bugs
- **Sécurité** pour les vulnérabilités corrigées 