from django.contrib import admin

from mailing.models import Client, Message, Mailing, MailingLog


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'email',)
    search_fields = ('first_name', 'last_name', 'email',)
    list_display_links = ('id', 'first_name',)


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'title',)
    search_fields = ('title', 'body',)
    list_display_links = ('id', 'title',)


@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = ('id', 'message', 'created_at', 'periodicity', 'mailing_status', 'message',)
    list_filter = ('periodicity', 'mailing_status', 'clients', 'message',)
    list_display_links = ('id', 'message',)


@admin.register(MailingLog)
class MailingLogAdmin(admin.ModelAdmin):
    list_display = ('id', 'sent_at', 'is_success', 'mailing',)
    list_filter = ('is_success', 'is_success', 'mailing',)
    search_fields = ('server_response',)
    list_display_links = ('id', 'sent_at',)
