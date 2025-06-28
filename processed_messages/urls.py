from django.urls import path
from .views import ProcessMessagesView, ProcessedMessagesListView

urlpatterns = [
    path('process-messages/', ProcessMessagesView.as_view(), name='process-messages'),
    path('processed-messages/', ProcessedMessagesListView.as_view(), name='processed-messages'),
] 