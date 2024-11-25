# Generated by Django 5.0.7 on 2024-08-26 14:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("mailing", "0007_alter_mailing_mailing_status_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="mailinglog",
            name="sent_at",
            field=models.DateTimeField(
                help_text="Укажите время отправки рассылки",
                verbose_name="Время отправки рассылки",
            ),
        ),
    ]
