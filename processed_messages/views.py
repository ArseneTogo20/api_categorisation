from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import ProcessedTransaction
from .serializers import ProcessedTransactionSerializer
from processed_messages.tasks import fetch_and_process_messages

class ProcessMessagesView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        fetch_and_process_messages.delay()
        return Response({"message": "Traitement lancé en arrière-plan."}, status=status.HTTP_202_ACCEPTED)

class ProcessedMessagesListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        page = int(request.query_params.get('page', 1))
        page_size = int(request.query_params.get('page_size', 20))
        qs = ProcessedTransaction.objects.all().order_by('-created_at')
        total = qs.count()
        start = (page - 1) * page_size
        end = start + page_size
        serializer = ProcessedTransactionSerializer(qs[start:end], many=True)
        return Response({
            "total": total,
            "page": page,
            "page_size": page_size,
            "results": serializer.data
        }) 