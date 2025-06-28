from celery import shared_task
from message_processing.models import Transaction
from processed_messages.models import ProcessedTransaction
from processed_messages.processing.category import categoriser_message
from processed_messages.processing.title_type import extract_type_and_title
from processed_messages.processing.amount_fee import extract_amount_and_fee
from decimal import Decimal
import logging

logger = logging.getLogger(__name__)

@shared_task
def fetch_and_process_messages():
    """
    Tâche Celery pour traiter automatiquement les nouveaux messages.
    Traite seulement les messages qui n'ont pas encore été traités.
    """
    logger.info("🚀 Début du traitement des messages...")
    
    # Récupérer tous les messages bruts non encore traités
    transactions = Transaction.objects.all()
    count_created = 0
    count_skipped = 0
    
    for txn in transactions:
        # Vérifier si déjà traité
        if ProcessedTransaction.objects.filter(id_message=str(txn.id)).exists():
            count_skipped += 1
            continue

        try:
            # Catégorisation
            category = categoriser_message(txn.message)
            type_, title = extract_type_and_title(txn.message, category)
            amount_fee = extract_amount_and_fee(txn.message, category)
            
            # Conversion en Decimal pour une meilleure précision
            amount = Decimal(str(amount_fee.get('amount', 0)))
            fee = Decimal(str(amount_fee.get('fee', 0)))
            amount_total = amount + fee

            # Enregistrement du message traité
            ProcessedTransaction.objects.create(
                id_message=str(txn.id),
                user_id=str(txn.user_id),
                message=txn.message,
                category=category,
                type=type_,
                title=title,
                amount=amount,
                fee=fee,
                amount_total=amount_total
            )
            count_created += 1
            logger.info(f"✅ Message traité: {txn.id} → {category} ({amount_total} FCFA)")
            
        except Exception as e:
            logger.error(f"❌ Erreur lors du traitement du message {txn.id}: {str(e)}")
            continue
    
    result_message = f"Traitement terminé. {count_created} messages traités, {count_skipped} ignorés."
    logger.info(f"🎯 {result_message}")
    return result_message 