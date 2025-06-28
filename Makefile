.PHONY: help install start stop restart logs test clean migrate superuser shell worker

# Variables
COMPOSE_FILE = docker-compose.yml
COMPOSE_PROD_FILE = docker-compose.prod.yml

help: ## Afficher cette aide
	@echo "Commandes disponibles:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install: ## Installer et configurer le projet
	@echo "🚀 Installation du projet..."
	cp .env.example .env
	@echo "📝 Veuillez configurer le fichier .env avec vos paramètres"
	@echo "✅ Installation terminée"

start: ## Démarrer les services de développement
	@echo "🚀 Démarrage des services..."
	docker-compose -f $(COMPOSE_FILE) up --build -d
	@echo "✅ Services démarrés"
	@echo "💡 Les workers Celery démarrent automatiquement"

stop: ## Arrêter les services
	@echo "🛑 Arrêt des services..."
	docker-compose -f $(COMPOSE_FILE) down
	@echo "✅ Services arrêtés"

restart: stop start ## Redémarrer les services

logs: ## Afficher les logs
	docker-compose -f $(COMPOSE_FILE) logs -f

logs-worker: ## Afficher les logs du worker Celery
	docker-compose -f $(COMPOSE_FILE) logs -f celery_worker

migrate: ## Appliquer les migrations
	@echo "🔄 Application des migrations..."
	docker-compose -f $(COMPOSE_FILE) exec api python manage.py migrate
	@echo "✅ Migrations appliquées"

superuser: ## Créer un superuser
	@echo "👤 Création d'un superuser..."
	docker-compose -f $(COMPOSE_FILE) exec api python manage.py createsuperuser

shell: ## Ouvrir un shell Django
	docker-compose -f $(COMPOSE_FILE) exec api python manage.py shell

worker: ## Lancer le worker Celery (manuel)
	@echo "⚙️ Lancement du worker Celery..."
	docker-compose -f $(COMPOSE_FILE) exec api celery -A projet_categorisation worker --loglevel=info

# 🚀 NOUVELLES COMMANDES POUR LE TRAITEMENT AUTOMATIQUE
process-messages: ## Traiter les messages manuellement
	@echo "🔍 Traitement des messages..."
	docker-compose -f $(COMPOSE_FILE) exec api python manage.py process_messages

process-messages-async: ## Traiter les messages en arrière-plan
	@echo "🚀 Traitement asynchrone des messages..."
	docker-compose -f $(COMPOSE_FILE) exec api python manage.py process_messages --async

process-messages-force: ## Forcer le traitement même sans nouveaux messages
	@echo "⚡ Traitement forcé des messages..."
	docker-compose -f $(COMPOSE_FILE) exec api python manage.py process_messages --force

stats: ## Afficher les statistiques de traitement
	@echo "📊 Statistiques du système..."
	docker-compose -f $(COMPOSE_FILE) exec api python manage.py process_messages --force

test: ## Lancer les tests
	@echo "🧪 Lancement des tests..."
	docker-compose -f $(COMPOSE_FILE) exec api python manage.py test

clean: ## Nettoyer les conteneurs et volumes
	@echo "🧹 Nettoyage..."
	docker-compose -f $(COMPOSE_FILE) down -v --remove-orphans
	docker system prune -f
	@echo "✅ Nettoyage terminé"

# Production commands
start-prod: ## Démarrer les services de production
	@echo "🚀 Démarrage des services de production..."
	docker-compose -f $(COMPOSE_PROD_FILE) up --build -d
	@echo "✅ Services de production démarrés"

stop-prod: ## Arrêter les services de production
	@echo "🛑 Arrêt des services de production..."
	docker-compose -f $(COMPOSE_PROD_FILE) down
	@echo "✅ Services de production arrêtés"

logs-prod: ## Afficher les logs de production
	docker-compose -f $(COMPOSE_PROD_FILE) logs -f

# Development helpers
makemigrations: ## Créer de nouvelles migrations
	@echo "📝 Création de nouvelles migrations..."
	docker-compose -f $(COMPOSE_FILE) exec api python manage.py makemigrations

collectstatic: ## Collecter les fichiers statiques
	@echo "📦 Collecte des fichiers statiques..."
	docker-compose -f $(COMPOSE_FILE) exec api python manage.py collectstatic --noinput

# Database commands
db-backup: ## Sauvegarder la base de données
	@echo "💾 Sauvegarde de la base de données..."
	docker-compose -f $(COMPOSE_FILE) exec db mysqldump -u root -p$(DB_ROOT_PASSWORD) $(DB_NAME) > backup_$(shell date +%Y%m%d_%H%M%S).sql

db-restore: ## Restaurer la base de données (usage: make db-restore FILE=backup.sql)
	@echo "🔄 Restauration de la base de données..."
	docker-compose -f $(COMPOSE_FILE) exec -T db mysql -u root -p$(DB_ROOT_PASSWORD) $(DB_NAME) < $(FILE)

# Monitoring
status: ## Afficher le statut des services
	@echo "📊 Statut des services:"
	docker-compose -f $(COMPOSE_FILE) ps

health: ## Vérifier la santé des services
	@echo "🏥 Vérification de la santé des services..."
	@curl -f http://localhost:8000/health/ || echo "❌ API non accessible"
	@docker-compose -f $(COMPOSE_FILE) exec db mysqladmin ping -h localhost || echo "❌ Base de données non accessible"
	@docker-compose -f $(COMPOSE_FILE) exec redis redis-cli ping || echo "❌ Redis non accessible" 