from django.contrib import admin

from mailing.models import Client, Message, Mailing, MailingLog


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "first_name",
        "last_name",
        "email",
        "owner",
    )
    list_filter = (
        "owner",
    )
    search_fields = (
        "first_name",
        "last_name",
        "email",
    )
    list_display_links = (
        "id",
        "first_name",
    )


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "owner",
    )
    list_filter = (
        "owner",
    )
    search_fields = (
        "title",
        "body",
    )
    list_display_links = (
        "id",
        "title",
    )


@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "message",
        "first_send_time",
        "periodicity",
        "mailing_status",
        "owner",
    )
    list_filter = (
        "periodicity",
        "mailing_status",
        "clients",
        "message",
        "owner",
    )
    list_display_links = (
        "id",
        "message",
    )


@admin.register(MailingLog)
class MailingLogAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "sent_at",
        "is_success",
        "mailing",
        "owner",
    )
    list_filter = (
        "is_success",
        "is_success",
        "mailing",
        "owner",
    )
    search_fields = ("server_response",)
    list_display_links = (
        "id",
        "sent_at",
    )
