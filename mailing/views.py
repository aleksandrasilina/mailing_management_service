from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView

from blog.models import Article
from mailing.forms import MailingForm, MailingModeratorForm
from mailing.models import Client, Message, Mailing, MailingLog


class IndexView(TemplateView):
    template_name = 'mailing/index.html'
    extra_context = {
        'title': 'Главная страница'
    }

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        user = self.request.user
        context_data['article_list'] = Article.objects.all().order_by('?')[:3]
        if user.is_authenticated:
            if user.is_superuser or user.groups.filter(name='manager').exists():
                context_data['mailing_count'] = Mailing.objects.count()
                context_data['active_mailing_count'] = Mailing.objects.filter(
                    mailing_status__in=['LAUNCHED', 'PAUSED']).count()
                context_data['client_count'] = Client.objects.count()
            else:
                context_data['mailing_count'] = Mailing.objects.filter(owner=user).count()
                context_data['active_mailing_count'] = Mailing.objects.filter(
                    owner=user, mailing_status__in=['LAUNCHED', 'PAUSED']).count()
                context_data['client_count'] = Client.objects.filter(owner=user).count()
        return context_data


class ClientListView(LoginRequiredMixin, ListView):
    model = Client
    paginate_by = 5
    extra_context = {
        'title': 'Клиенты'
    }

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        user = self.request.user
        if not user.has_perm('mailing.view_client'):
            queryset = queryset.filter(owner=user)
        return queryset


class ClientDetailView(LoginRequiredMixin, DetailView):
    model = Client

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = context['client']
        return context


class ClientCreateView(LoginRequiredMixin, CreateView):
    model = Client
    fields = ('first_name', 'last_name', 'email', 'avatar', 'comment',)
    success_url = reverse_lazy('mailing:client_list')
    extra_context = {
        'title': 'Создание клиента'
    }

    def form_valid(self, form):
        client = form.save()
        user = self.request.user
        client.owner = user
        client.save()
        return super().form_valid(form)


class ClientUpdateView(LoginRequiredMixin, UpdateView):
    model = Client
    fields = ('first_name', 'last_name', 'email', 'avatar', 'comment',)
    success_url = reverse_lazy('mailing:client_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Редактирование клиента: {context['client']}'
        return context


class ClientDeleteView(LoginRequiredMixin, DeleteView):
    model = Client
    success_url = reverse_lazy('mailing:client_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Удаление клиента: {context['client']}'
        return context


class MessageListView(LoginRequiredMixin, ListView):
    model = Message
    paginate_by = 5
    extra_context = {
        'title': 'Сообщения'
    }

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        user = self.request.user
        if not user.has_perm('mailing.view_message'):
            queryset = queryset.filter(owner=user)
        return queryset


class MessageDetailView(LoginRequiredMixin, DetailView):
    model = Message

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = context['message']
        return context


class MessageCreateView(LoginRequiredMixin, CreateView):
    model = Message
    fields = ('title', 'body',)
    success_url = reverse_lazy('mailing:message_list')
    extra_context = {
        'title': 'Создание сообщения'
    }

    def form_valid(self, form):
        message = form.save()
        user = self.request.user
        message.owner = user
        message.save()
        return super().form_valid(form)


class MessageUpdateView(LoginRequiredMixin, UpdateView):
    model = Message
    fields = ('title', 'body',)
    success_url = reverse_lazy('mailing:message_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Редактирование сообщения: {context['message']}'
        return context


class MessageDeleteView(LoginRequiredMixin, DeleteView):
    model = Message
    success_url = reverse_lazy('mailing:message_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Удаление сообщения: {context['message']}'
        return context


class MailingListView(LoginRequiredMixin, ListView):
    model = Mailing
    paginate_by = 5
    extra_context = {
        'title': 'Рассылки'
    }

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        user = self.request.user
        if not user.has_perm('mailing.view_mailing'):
            queryset = queryset.filter(owner=self.request.user)
        return queryset


class MailingDetailView(LoginRequiredMixin, DetailView):
    model = Mailing

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = context['mailing']
        return context


class MailingCreateView(LoginRequiredMixin, CreateView):
    model = Mailing
    success_url = reverse_lazy('mailing:mailing_list')
    form_class = MailingForm
    extra_context = {
        'title': 'Создание рассылки'
    }

    def form_valid(self, form):
        mailing = form.save()
        user = self.request.user
        mailing.owner = user
        mailing.mailing_status = 'CREATED'
        mailing.save()
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs


class MailingUpdateView(LoginRequiredMixin, UpdateView):
    model = Mailing
    success_url = reverse_lazy('mailing:mailing_list')
    form_class = MailingForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def get_form_class(self):
        user = self.request.user
        if user == self.object.owner or user.is_superuser:
            return MailingForm
        if user.has_perm("mailing.change_mailing_status"):
            return MailingModeratorForm
        raise PermissionDenied

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Редактирование рассылки: {context['mailing']}'
        return context


class MailingDeleteView(LoginRequiredMixin, DeleteView):
    model = Mailing
    success_url = reverse_lazy('mailing:mailing_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Удаление рассылки: {context['mailing']}'
        return context


class MailingLogListView(LoginRequiredMixin, ListView):
    model = MailingLog
    paginate_by = 5
    extra_context = {
        'title': 'Статистика'
    }

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        user = self.request.user
        if not user.has_perm('mailing.view_mailinglog'):
            queryset = queryset.filter(owner=self.request.user)
        return queryset


class MailingLogDetailView(LoginRequiredMixin, DetailView):
    model = MailingLog

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = context['mailinglog']
        return context
