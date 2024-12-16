# Generated by Django 4.2.2 on 2024-09-02 21:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("mailing", "0019_alter_mailing_options"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="client",
            options={
                "ordering": ("owner", "last_name"),
                "verbose_name": "Клиент",
                "verbose_name_plural": "Клиенты",
            },
        ),
        migrations.AlterModelOptions(
            name="mailing",
            options={
                "ordering": ("-first_send_time",),
                "permissions": [
                    ("can_change_mailing_status", "Can change mailing status")
                ],
                "verbose_name": "Рассылка",
                "verbose_name_plural": "Рассылки",
            },
        ),
        migrations.AlterModelOptions(
            name="message",
            options={
                "ordering": ("owner", "title"),
                "verbose_name": "Сообщение",
                "verbose_name_plural": "Сообщения",
            },
        ),
    ]
