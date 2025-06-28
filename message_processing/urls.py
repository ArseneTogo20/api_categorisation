from django.urls import path
from .views import TransactionBulkCreateView, TransactionListView

app_name = 'message_processing'

urlpatterns = [
    # GET /api/get-all-messages/ - Liste des messages
    path('get-all-messages/', TransactionListView.as_view(), name='get_all_messages'),

    # POST /api/messages/enregister/ - Création en masse de messages
    path('messages/enregister/', TransactionBulkCreateView.as_view(), name='message_bulk_create'),
] 