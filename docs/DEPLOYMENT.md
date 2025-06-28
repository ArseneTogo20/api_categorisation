# Guide de Déploiement

## Vue d'ensemble

Ce guide vous accompagne dans le déploiement de l'API de Catégorisation de Messages en production.

## Prérequis

- Docker et Docker Compose installés
- Serveur Linux (Ubuntu 20.04+ recommandé)
- 2GB RAM minimum, 4GB recommandé
- 10GB espace disque minimum
- Domaine configuré (optionnel mais recommandé)

## Déploiement Rapide

### 1. Cloner le repository

```bash
git clone https://github.com/votre-username/projet_categorisation.git
cd projet_categorisation
```

### 2. Configuration

```bash
# Copier le fichier d'environnement
cp .env.example .env

# Éditer la configuration
nano .env
```

Configuration minimale pour `.env` :
```env
DEBUG=False
SECRET_KEY=votre-super-secret-key-change-this
DB_HOST=db
DB_NAME=projet_categorisation
DB_USER=user_app
DB_PASSWORD=password_app_securise
DB_ROOT_PASSWORD=root_password_securise
DB_PORT=3306
REDIS_URL=redis://redis:6379/0
REDIS_PASSWORD=redis_password_securise
ALLOWED_HOSTS=votre-domaine.com,www.votre-domaine.com
```

### 3. Déploiement

```bash
# Utiliser le script de déploiement
./scripts/deploy.sh production

# Ou manuellement
docker-compose -f docker-compose.prod.yml up --build -d
```

### 4. Vérification

```bash
# Vérifier les services
docker-compose -f docker-compose.prod.yml ps

# Vérifier la santé de l'API
curl http://localhost/health/

# Voir les logs
docker-compose -f docker-compose.prod.yml logs -f
```

## Configuration SSL/TLS

### 1. Obtenir un certificat SSL

```bash
# Installer Certbot
sudo apt update
sudo apt install certbot

# Obtenir un certificat Let's Encrypt
sudo certbot certonly --standalone -d votre-domaine.com -d www.votre-domaine.com
```

### 2. Configurer Nginx

```bash
# Copier les certificats
sudo cp /etc/letsencrypt/live/votre-domaine.com/fullchain.pem nginx/ssl/cert.pem
sudo cp /etc/letsencrypt/live/votre-domaine.com/privkey.pem nginx/ssl/key.pem

# Redémarrer les services
docker-compose -f docker-compose.prod.yml restart nginx
```

### 3. Renouvellement automatique

```bash
# Ajouter au crontab
sudo crontab -e

# Ajouter cette ligne
0 12 * * * /usr/bin/certbot renew --quiet && cp /etc/letsencrypt/live/votre-domaine.com/fullchain.pem /path/to/project/nginx/ssl/cert.pem && cp /etc/letsencrypt/live/votre-domaine.com/privkey.pem /path/to/project/nginx/ssl/key.pem && docker-compose -f /path/to/project/docker-compose.prod.yml restart nginx
```

## Configuration de Production

### Variables d'environnement critiques

```env
# Sécurité
DEBUG=False
SECRET_KEY=generate-a-secure-secret-key
ALLOWED_HOSTS=votre-domaine.com,www.votre-domaine.com

# Base de données
DB_PASSWORD=password-tres-securise
DB_ROOT_PASSWORD=root-password-tres-securise

# Redis
REDIS_PASSWORD=redis-password-securise

# JWT
JWT_ACCESS_TOKEN_LIFETIME=5
JWT_REFRESH_TOKEN_LIFETIME=1
```

### Génération d'une clé secrète sécurisée

```bash
# Générer une clé secrète
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

## Monitoring et Logs

### 1. Logs Docker

```bash
# Logs de tous les services
docker-compose -f docker-compose.prod.yml logs -f

# Logs d'un service spécifique
docker-compose -f docker-compose.prod.yml logs -f api
docker-compose -f docker-compose.prod.yml logs -f nginx
```

### 2. Monitoring de la base de données

```bash
# Accéder à MySQL
docker-compose -f docker-compose.prod.yml exec db mysql -u root -p

# Vérifier les performances
SHOW PROCESSLIST;
SHOW STATUS LIKE 'Threads_connected';
```

### 3. Monitoring Redis

```bash
# Accéder à Redis
docker-compose -f docker-compose.prod.yml exec redis redis-cli

# Vérifier les statistiques
INFO
INFO memory
```

### 4. Monitoring Celery

```bash
# Vérifier les workers
docker-compose -f docker-compose.prod.yml exec api celery -A projet_categorisation inspect active

# Vérifier les tâches en attente
docker-compose -f docker-compose.prod.yml exec api celery -A projet_categorisation inspect reserved
```

## Sauvegarde et Restauration

### 1. Sauvegarde automatique

```bash
# Créer un script de sauvegarde
cat > /root/backup.sh << 'EOF'
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/backups"
mkdir -p $BACKUP_DIR

# Sauvegarde de la base de données
docker-compose -f /path/to/project/docker-compose.prod.yml exec -T db mysqldump -u root -p${DB_ROOT_PASSWORD} ${DB_NAME} > $BACKUP_DIR/db_backup_$DATE.sql

# Sauvegarde des fichiers
tar -czf $BACKUP_DIR/files_backup_$DATE.tar.gz /path/to/project

# Nettoyer les anciennes sauvegardes (garder 7 jours)
find $BACKUP_DIR -name "*.sql" -mtime +7 -delete
find $BACKUP_DIR -name "*.tar.gz" -mtime +7 -delete
EOF

chmod +x /root/backup.sh

# Ajouter au crontab (sauvegarde quotidienne à 2h du matin)
echo "0 2 * * * /root/backup.sh" | sudo crontab -
```

### 2. Restauration

```bash
# Restaurer la base de données
docker-compose -f docker-compose.prod.yml exec -T db mysql -u root -p${DB_ROOT_PASSWORD} ${DB_NAME} < backup.sql

# Restaurer les fichiers
tar -xzf files_backup.tar.gz -C /
```

## Mise à jour

### 1. Mise à jour automatique

```bash
# Créer un script de mise à jour
cat > /root/update.sh << 'EOF'
#!/bin/bash
cd /path/to/project

# Sauvegarde avant mise à jour
./scripts/deploy.sh backup

# Pull des dernières modifications
git pull origin main

# Redéploiement
./scripts/deploy.sh production

# Vérification
curl -f http://localhost/health/ || exit 1
EOF

chmod +x /root/update.sh
```

### 2. Mise à jour manuelle

```bash
# Arrêter les services
docker-compose -f docker-compose.prod.yml down

# Pull des modifications
git pull origin main

# Redémarrer avec les nouvelles images
docker-compose -f docker-compose.prod.yml up --build -d

# Appliquer les migrations
docker-compose -f docker-compose.prod.yml exec api python manage.py migrate
```

## Sécurité

### 1. Firewall

```bash
# Installer UFW
sudo apt install ufw

# Configuration de base
sudo ufw default deny incoming
sudo ufw default allow outgoing

# Autoriser SSH
sudo ufw allow ssh

# Autoriser HTTP et HTTPS
sudo ufw allow 80
sudo ufw allow 443

# Activer le firewall
sudo ufw enable
```

### 2. Mise à jour du système

```bash
# Mise à jour automatique
sudo apt update && sudo apt upgrade -y

# Configuration des mises à jour automatiques
sudo apt install unattended-upgrades
sudo dpkg-reconfigure -plow unattended-upgrades
```

### 3. Surveillance

```bash
# Installer des outils de monitoring
sudo apt install htop iotop nethogs

# Surveillance des logs
tail -f /var/log/syslog | grep -i error
```

## Performance

### 1. Optimisation Nginx

```nginx
# Ajouter dans nginx.conf
worker_processes auto;
worker_connections 1024;
keepalive_timeout 65;
gzip on;
gzip_types text/plain text/css application/json application/javascript;
```

### 2. Optimisation Django

```python
# settings.py
DEBUG = False
ALLOWED_HOSTS = ['votre-domaine.com']
STATIC_ROOT = '/app/static/'
MEDIA_ROOT = '/app/media/'

# Cache
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': 'redis://redis:6379/1',
    }
}
```

### 3. Optimisation Celery

```python
# settings.py
CELERY_WORKER_CONCURRENCY = 4
CELERY_TASK_TIME_LIMIT = 30 * 60
CELERY_TASK_SOFT_TIME_LIMIT = 25 * 60
```

## Dépannage

### Problèmes courants

1. **Service ne démarre pas**
   ```bash
   docker-compose -f docker-compose.prod.yml logs service_name
   ```

2. **Base de données inaccessible**
   ```bash
   docker-compose -f docker-compose.prod.yml exec db mysql -u root -p
   ```

3. **Redis inaccessible**
   ```bash
   docker-compose -f docker-compose.prod.yml exec redis redis-cli ping
   ```

4. **Worker Celery ne fonctionne pas**
   ```bash
   docker-compose -f docker-compose.prod.yml exec api celery -A projet_categorisation worker --loglevel=info
   ```

### Commandes utiles

```bash
# Vérifier l'état des services
docker-compose -f docker-compose.prod.yml ps

# Redémarrer un service
docker-compose -f docker-compose.prod.yml restart service_name

# Voir les ressources utilisées
docker stats

# Nettoyer les conteneurs non utilisés
docker system prune -f
```

## Support

En cas de problème :
1. Consultez les logs : `docker-compose -f docker-compose.prod.yml logs -f`
2. Vérifiez la santé : `curl http://localhost/health/`
3. Créez une issue sur GitHub
4. Contactez l'équipe de support 