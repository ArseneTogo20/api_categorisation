from rest_framework import serializers
from .models import Transaction
import uuid

class TransactionSerializer(serializers.ModelSerializer):
    """
    Sérialiseur pour une seule transaction.
    Valide que user_id est un UUID et que message est présent.
    """
    user_id = serializers.UUIDField()
    message = serializers.CharField(max_length=512)

    class Meta:
        model = Transaction
        fields = ['user_id', 'message']


class TransactionResponseSerializer(serializers.ModelSerializer):
    """
    Sérialiseur pour la réponse qui inclut l'ID généré automatiquement.
    """
    id_message = serializers.UUIDField(source='id', read_only=True)
    
    class Meta:
        model = Transaction
        fields = ['id_message', 'user_id', 'message', 'created_at']


class TransactionBulkSerializer(serializers.ListSerializer):
    """
    Sérialiseur pour la requête en masse.
    Attend directement une liste d'objets transaction.
    """
    child = TransactionSerializer()

    def validate(self, value):
        """
        Vérifie que la liste des transactions n'est pas vide.
        """
        if not value:
            raise serializers.ValidationError("La liste des transactions ne peut pas être vide.")
        return value 