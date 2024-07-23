from django.urls import path

from mailing.apps import MailingConfig
from mailing.views import ClientListView

app_name = MailingConfig.name

urlpatterns = [
    path('', ClientListView.as_view(), name='client_list'),
]
