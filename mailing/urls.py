from django.urls import path

from mailing.apps import MailingConfig
from mailing.views import ClientListView, ClientDetailView

app_name = MailingConfig.name

urlpatterns = [
    path('', ClientListView.as_view(), name='client_list'),
    path('client_detail/<int:pk>/', ClientDetailView.as_view(), name='client_detail'),
]
