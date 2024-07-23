from django.shortcuts import render
from django.views.generic import ListView, DetailView

from mailing.models import Client


class ClientListView(ListView):
    model = Client


class ClientDetailView(DetailView):
    model = Client
