# Generated by Django 5.0.7 on 2024-07-24 07:29

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mailing', '0005_alter_mailing_mailing_status_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mailing',
            name='client',
        ),
        migrations.AddField(
            model_name='mailing',
            name='clients',
            field=models.ManyToManyField(help_text='Выберите клиентов для рассылки', related_name='mailings', to='mailing.client', verbose_name='Клиенты рассылки'),
        ),
        migrations.AlterField(
            model_name='mailing',
            name='message',
            field=models.ForeignKey(help_text='Выберите сообщение для рассылки', on_delete=django.db.models.deletion.CASCADE, related_name='mailings', to='mailing.message', verbose_name='Сообщение рассылки'),
        ),
    ]
