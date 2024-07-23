# Generated by Django 5.0.7 on 2024-07-23 06:23

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(help_text='Введите имя клиента', max_length=100, verbose_name='Имя')),
                ('last_name', models.CharField(help_text='Введите фамилию клиента', max_length=150, verbose_name='Фамилия')),
                ('email', models.EmailField(help_text='Введите электронную почту клиента', max_length=254, unique=True, verbose_name='Почта')),
            ],
            options={
                'verbose_name': 'Клиент',
                'verbose_name_plural': 'Клиенты',
                'ordering': ('last_name',),
            },
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(help_text='Введите тему сообщения', max_length=200, verbose_name='Тема сообщения')),
                ('body', models.TextField(help_text='Напишите сообщение', verbose_name='Содержание сообщения')),
            ],
            options={
                'verbose_name': 'Сообщение',
                'verbose_name_plural': 'Сообщения',
                'ordering': ('title',),
            },
        ),
        migrations.CreateModel(
            name='Mailing',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Введите дату создания рассылки')),
                ('periodicity', models.CharField(choices=[(1, 'раз в день'), (2, 'раз в неделю'), (3, 'раз в месяц')], help_text='Выберите периодичность рассылки', max_length=20, verbose_name='Периодичность рассылки')),
                ('mailing_status', models.CharField(choices=[(1, 'создана'), (2, 'запущена'), (3, 'завершена')], help_text='Выберите статус рассылки', max_length=100, verbose_name='Статус рассылки')),
                ('client', models.ManyToManyField(help_text='Выберите клиентов для рассылки', related_name='clients', to='mailing.client', verbose_name='Клиенты рассылки')),
                ('message', models.ForeignKey(help_text='Выберите сообщение для рассылки', on_delete=django.db.models.deletion.CASCADE, related_name='messages', to='mailing.message', verbose_name='Сообщение рассылки')),
            ],
            options={
                'verbose_name': 'Рассылка',
                'verbose_name_plural': 'Рассылки',
                'ordering': ('-created_at',),
            },
        ),
        migrations.CreateModel(
            name='MailingLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sent_at', models.DateTimeField(auto_now_add=True, help_text='Укажите время отправки рассылки', verbose_name='Время отправки рассылки')),
                ('is_success', models.BooleanField(default=False, help_text='Укажите, успешно ли отправлена рассылка', verbose_name='Успешно')),
                ('server_response', models.TextField(blank=True, null=True, verbose_name='Ответ сервера')),
                ('mailing', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='logs', to='mailing.mailing', verbose_name='Рассылка')),
            ],
            options={
                'verbose_name': 'Лог рассылки',
                'verbose_name_plural': 'Логи рассылок',
                'ordering': ('-sent_at',),
            },
        ),
    ]