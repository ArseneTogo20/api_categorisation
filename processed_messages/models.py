import uuid
from django.db import models
from decimal import Decimal

class ProcessedTransaction(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    id_message = models.CharField(max_length=64, db_index=True, unique=True)
    user_id = models.CharField(max_length=64, db_index=True)
    message = models.TextField()
    category = models.CharField(max_length=32, null=True, blank=True)
    type = models.CharField(max_length=32, null=True, blank=True)
    title = models.CharField(max_length=128, null=True, blank=True)
    amount = models.DecimalField(max_digits=15, decimal_places=2, default=Decimal('0.00'), help_text="Montant principal en FCFA")
    fee = models.DecimalField(max_digits=15, decimal_places=2, default=Decimal('0.00'), help_text="Frais en FCFA")
    amount_total = models.DecimalField(max_digits=15, decimal_places=2, default=Decimal('0.00'), help_text="Montant total (principal + frais) en FCFA")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Transaction traitée"
        verbose_name_plural = "Transactions traitées"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.id_message} | {self.category} | {self.amount_total} FCFA"
    
    def save(self, *args, **kwargs):
        # Calcul automatique du montant total si pas défini
        if self.amount_total == Decimal('0.00'):
            self.amount_total = self.amount + self.fee
        super().save(*args, **kwargs) 