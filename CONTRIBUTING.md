# Guide de Contribution

Merci de votre intérêt pour contribuer à l'API de Catégorisation de Messages ! 

## 🚀 Comment Contribuer

### 1. Fork et Clone

1. Fork ce repository sur GitHub
2. Clone votre fork localement :
   ```bash
   git clone https://github.com/votre-username/projet_categorisation.git
   cd projet_categorisation
   ```

### 2. Configuration de l'environnement

1. Assurez-vous d'avoir Docker et Docker Compose installés
2. Créez un fichier `.env` basé sur `.env.example`
3. Démarrez l'environnement de développement :
   ```bash
   docker-compose up --build -d
   docker-compose exec api python manage.py migrate
   docker-compose exec api python manage.py createsuperuser
   ```

### 3. Créer une branche

Créez une branche pour votre fonctionnalité :
```bash
git checkout -b feature/nom-de-votre-fonctionnalite
```

### 4. Développement

- Suivez les conventions de code Python (PEP 8)
- Ajoutez des tests pour les nouvelles fonctionnalités
- Documentez votre code
- Testez vos modifications localement

### 5. Tests

Avant de soumettre votre contribution :
```bash
# Tests unitaires
docker-compose exec api python manage.py test

# Tests de l'API
python test_api.py  # Si vous avez des tests d'intégration
```

### 6. Commit et Push

```bash
git add .
git commit -m "feat: ajouter une nouvelle fonctionnalité"
git push origin feature/nom-de-votre-fonctionnalite
```

### 7. Pull Request

1. Allez sur GitHub et créez une Pull Request
2. Remplissez le template de PR
3. Attendez la review

## 📋 Standards de Code

### Python
- Suivez PEP 8
- Utilisez des docstrings pour les fonctions et classes
- Nommez les variables et fonctions de manière descriptive
- Limitez la longueur des lignes à 79 caractères

### Django
- Utilisez les bonnes pratiques Django
- Créez des migrations pour les changements de modèles
- Utilisez les sérialiseurs DRF pour les APIs
- Validez les données d'entrée

### Git
- Utilisez des messages de commit conventionnels
- Faites des commits atomiques
- Utilisez des branches descriptives

## 🧪 Tests

### Tests Unitaires
```bash
docker-compose exec api python manage.py test
```

### Tests d'Intégration
```bash
# Test complet de l'API
python test_api.py
```

### Couverture de Code
```bash
docker-compose exec api coverage run --source='.' manage.py test
docker-compose exec api coverage report
```

## 📝 Documentation

- Mettez à jour le README.md si nécessaire
- Documentez les nouvelles fonctionnalités
- Ajoutez des exemples d'utilisation
- Mettez à jour le CHANGELOG.md

## 🐛 Signaler un Bug

1. Vérifiez que le bug n'a pas déjà été signalé
2. Créez une issue avec le template de bug
3. Incluez les étapes pour reproduire le bug
4. Ajoutez les logs d'erreur si disponibles

## 💡 Proposer une Fonctionnalité

1. Créez une issue avec le template de feature request
2. Décrivez clairement la fonctionnalité souhaitée
3. Expliquez pourquoi cette fonctionnalité serait utile
4. Proposez une implémentation si possible

## 🔧 Configuration de l'environnement de développement

### Variables d'environnement
```env
DEBUG=True
SECRET_KEY=your-secret-key
DATABASE_URL=mysql://user:password@db:3306/dbname
REDIS_URL=redis://redis:6379/0
```

### Commandes utiles
```bash
# Démarrer l'environnement
docker-compose up -d

# Voir les logs
docker-compose logs -f api

# Accéder au shell Django
docker-compose exec api python manage.py shell

# Créer une migration
docker-compose exec api python manage.py makemigrations

# Appliquer les migrations
docker-compose exec api python manage.py migrate

# Lancer le worker Celery
docker-compose exec api celery -A projet_categorisation worker --loglevel=info
```

## 📞 Support

Si vous avez des questions ou besoin d'aide :
- Créez une issue sur GitHub
- Consultez la documentation dans le README.md
- Vérifiez les issues existantes

## 🎉 Remerciements

Merci à tous les contributeurs qui participent à l'amélioration de ce projet !

---

**Note** : Ce guide est en constante évolution. N'hésitez pas à proposer des améliorations ! 