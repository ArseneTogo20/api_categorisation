from django.core.management.base import BaseCommand
from django.db import transaction
from message_processing.models import Transaction
from processed_messages.models import ProcessedTransaction
from processed_messages.tasks import fetch_and_process_messages
import time


class Command(BaseCommand):
    help = 'Traite les messages non traités et affiche les statistiques'

    def add_arguments(self, parser):
        parser.add_argument(
            '--force',
            action='store_true',
            help='Forcer le traitement même si aucun nouveau message',
        )
        parser.add_argument(
            '--async',
            action='store_true',
            help='Lancer le traitement en arrière-plan (Celery)',
        )

    def handle(self, *args, **options):
        self.stdout.write("🔍 Analyse du système de traitement...")
        
        # Statistiques
        total_messages = Transaction.objects.count()
        total_processed = ProcessedTransaction.objects.count()
        pending_messages = total_messages - total_processed
        
        self.stdout.write(f"📊 Statistiques:")
        self.stdout.write(f"   • Messages totaux: {total_messages}")
        self.stdout.write(f"   • Messages traités: {total_processed}")
        self.stdout.write(f"   • Messages en attente: {pending_messages}")
        
        if pending_messages == 0 and not options['force']:
            self.stdout.write(self.style.WARNING("⚠️  Aucun nouveau message à traiter."))
            return
        
        if options['async']:
            self.stdout.write("🚀 Lancement du traitement asynchrone...")
            task = fetch_and_process_messages.delay()
            self.stdout.write(f"✅ Tâche Celery lancée avec l'ID: {task.id}")
            self.stdout.write("💡 Utilisez 'celery -A projet_categorisation flower' pour surveiller les tâches")
        else:
            self.stdout.write("⚡ Traitement synchrone en cours...")
            start_time = time.time()
            
            result = fetch_and_process_messages()
            
            end_time = time.time()
            duration = end_time - start_time
            
            self.stdout.write(f"✅ {result}")
            self.stdout.write(f"⏱️  Durée: {duration:.2f} secondes")
        
        # Statistiques finales
        new_total_processed = ProcessedTransaction.objects.count()
        newly_processed = new_total_processed - total_processed
        
        self.stdout.write(f"🎯 Résultat final:")
        self.stdout.write(f"   • Nouveaux messages traités: {newly_processed}")
        self.stdout.write(f"   • Total traité: {new_total_processed}")
        
        self.stdout.write(self.style.SUCCESS("✅ Traitement terminé avec succès!")) 