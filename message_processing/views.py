from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.core.paginator import Paginator
from django.db.models import Q

from .models import Transaction
from .serializers import TransactionBulkSerializer, TransactionResponseSerializer
from processed_messages.tasks import fetch_and_process_messages

class TransactionListView(APIView):
    """
    Vue pour récupérer la liste des transactions avec pagination et filtres.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        # Récupérer les paramètres de requête
        page = request.query_params.get('page', 1)
        page_size = min(int(request.query_params.get('page_size', 10)), 100)  # Max 100 par page
        user_id = request.query_params.get('user_id')
        search = request.query_params.get('search')
        
        # Construire la requête de base
        queryset = Transaction.objects.all()
        
        # Appliquer les filtres
        if user_id:
            try:
                queryset = queryset.filter(user_id=user_id)
            except ValueError:
                return Response({
                    "status": "error",
                    "message": "user_id doit être un UUID valide"
                }, status=status.HTTP_400_BAD_REQUEST)
        
        if search:
            queryset = queryset.filter(
                Q(message__icontains=search) |
                Q(user_id__icontains=search)
            )
        
        # Pagination
        paginator = Paginator(queryset, page_size)
        try:
            transactions_page = paginator.page(page)
        except:
            return Response({
                "status": "error",
                "message": "Page invalide"
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Sérialiser les données
        transactions_data = TransactionResponseSerializer(
            transactions_page.object_list, many=True
        ).data
        
        return Response({
            "status": "success",
            "total_count": paginator.count,
            "total_pages": paginator.num_pages,
            "current_page": int(page),
            "page_size": page_size,
            "has_next": transactions_page.has_next(),
            "has_previous": transactions_page.has_previous(),
            "transactions": transactions_data
        }, status=status.HTTP_200_OK)


class TransactionBulkCreateView(APIView):
    """
    Vue pour enregistrer des transactions en masse.
    Cet endpoint est optimisé pour traiter un grand volume de transactions
    et ignorer les doublons en se basant sur la contrainte d'unicité
    de la base de données sur (user_id, message).
    """
    permission_classes = [IsAuthenticated] # Protège l'endpoint

    def post(self, request, *args, **kwargs):
        # 1. Valider la structure de la requête
        bulk_serializer = TransactionBulkSerializer(data=request.data)
        if not bulk_serializer.is_valid():
            return Response({
                "status": "error",
                "message": "Format de requête invalide.",
                "errors": bulk_serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

        # 2. Préparer les données pour l'insertion
        transactions_data = bulk_serializer.validated_data
        total_received = len(transactions_data)
        
        # Créer une liste d'objets Transaction non sauvegardés
        # On utilise un set pour dédoublonner les paires (user_id, message) DANS la requête elle-même
        # pour optimiser le nombre d'objets envoyés à la base de données.
        unique_transactions_in_payload = {(t['user_id'], t['message']) for t in transactions_data}
        
        transactions_to_create = [
            Transaction(user_id=user_id, message=message)
            for user_id, message in unique_transactions_in_payload
        ]

        # Compter les transactions déjà existantes
        existing_transactions = set(Transaction.objects.filter(
            user_id__in=[t.user_id for t in transactions_to_create]
        ).values_list('user_id', 'message'))

        # Filtrer pour ne garder que les nouvelles transactions
        new_transactions = [
            t for t in transactions_to_create
            if (t.user_id, t.message) not in existing_transactions
        ]
        
        try:
            if new_transactions:
                Transaction.objects.bulk_create(new_transactions)
            
            created_count = len(new_transactions)
            duplicates_count = total_received - created_count

            # Sérialiser les transactions créées pour inclure leurs IDs
            created_transactions_data = []
            if new_transactions:
                # Récupérer les transactions créées avec leurs IDs
                created_transactions = Transaction.objects.filter(
                    user_id__in=[t.user_id for t in new_transactions],
                    message__in=[t.message for t in new_transactions]
                ).order_by('-created_at')[:created_count]
                
                created_transactions_data = TransactionResponseSerializer(
                    created_transactions, many=True
                ).data

            # 🚀 NOUVEAU : Déclencher automatiquement le traitement si des messages ont été créés
            if created_count > 0:
                fetch_and_process_messages.delay()

            return Response({
                "status": "success",
                "created": created_count,
                "duplicates": duplicates_count,
                "total_received": total_received,
                "transactions": created_transactions_data,
                "processing_triggered": created_count > 0  # Indique si le traitement a été lancé
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({
                "status": "error",
                "message": f"Une erreur interne est survenue: {e}"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
