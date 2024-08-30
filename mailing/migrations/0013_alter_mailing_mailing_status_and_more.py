# Generated by Django 5.0.7 on 2024-08-27 11:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("mailing", "0012_alter_mailing_options_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="mailing",
            name="mailing_status",
            field=models.CharField(
                choices=[
                    ("created", "создана"),
                    ("launched", "запущена"),
                    ("completed", "завершена"),
                ],
                default="created",
                help_text="Выберите статус рассылки",
                max_length=100,
                verbose_name="Статус рассылки",
            ),
        ),
        migrations.AlterField(
            model_name="mailing",
            name="periodicity",
            field=models.CharField(
                choices=[
                    ("once a day", "раз в день"),
                    ("once a week", "раз в неделю"),
                    ("once a month", "раз в месяц"),
                ],
                help_text="Выберите периодичность рассылки",
                max_length=20,
                verbose_name="Периодичность рассылки",
            ),
        ),
    ]