import uuid
from django.db import models

class Transaction(models.Model):
    """
    Représente une transaction financière reçue d'une application externe.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_id = models.UUIDField(db_index=True, help_text="Identifiant UUID de l'utilisateur externe")
    message = models.CharField(max_length=512, help_text="Contenu brut du message de la transaction")
    created_at = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name="Date de réception")

    class Meta:
        # Contrainte d'unicité pour garantir qu'une même transaction (même utilisateur et même message)
        # ne soit pas enregistrée plusieurs fois.
        constraints = [
            models.UniqueConstraint(fields=['user_id', 'message'], name='unique_user_message_transaction')
        ]
        verbose_name = "Transaction"
        verbose_name_plural = "Transactions"
        ordering = ['-created_at']

    def __str__(self):
        return f"Transaction de {self.user_id} le {self.created_at.strftime('%Y-%m-%d %H:%M')}"
