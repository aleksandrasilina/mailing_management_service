from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView

from mailing.models import Client


class ClientListView(ListView):
    model = Client


class ClientDetailView(DetailView):
    model = Client


class ClientCreateView(CreateView):
    model = Client
    fields = ('first_name', 'last_name', 'email', 'avatar', 'comment',)
    success_url = reverse_lazy('mailing:client_list')


class ClientUpdateView(UpdateView):
    model = Client
    fields = ('first_name', 'last_name', 'email', 'avatar', 'comment',)
    success_url = reverse_lazy('mailing:client_list')
