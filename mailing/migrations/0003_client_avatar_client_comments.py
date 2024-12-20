# Generated by Django 5.0.7 on 2024-07-23 08:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mailing', '0002_alter_mailing_mailing_status_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='avatar',
            field=models.ImageField(blank=True, help_text='Загрузите аватар клиента', null=True, upload_to='mailing/avatars/', verbose_name='Аватар'),
        ),
        migrations.AddField(
            model_name='client',
            name='comments',
            field=models.TextField(blank=True, help_text='Введите комментарий', null=True, verbose_name='Комментарий'),
        ),
    ]
