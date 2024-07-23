from django.db import models

from django.db import models


NULLABLE = {'blank': True, 'null': True}
PERIODICITY_CHOICES = (
    (1, 'раз в день',),
    (2, 'раз в неделю',),
    (3, 'раз в месяц',)
)
MAILING_STATUS_CHOICES = (
    (1, 'создана',),
    (2, 'запущена',),
    (3, 'завершена',)
)


class Client(models.Model):
    first_name = models.CharField(max_length=100, verbose_name='Имя', help_text='Введите имя клиента')
    last_name = models.CharField(max_length=150, verbose_name='Фамилия', help_text='Введите фамилию клиента')
    email = models.EmailField(verbose_name='Почта', unique=True, help_text='Введите электронную почту клиента')

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'
        ordering = ('last_name',)


class Message(models.Model):
    title = models.CharField(max_length=200, verbose_name='Тема сообщения', help_text='Введите тему сообщения')
    body = models.TextField(verbose_name='Содержание сообщения', help_text='Напишите сообщение')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'
        ordering = ('title',)


class Mailing(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Введите дату создания рассылки')
    periodicity = models.CharField(max_length=20, verbose_name='Периодичность рассылки',
                                   help_text='Выберите периодичность рассылки', choices=PERIODICITY_CHOICES)
    mailing_status = models.CharField(max_length=100, verbose_name='Статус рассылки',
                                      help_text='Выберите статус рассылки', choices=MAILING_STATUS_CHOICES)
    client = models.ManyToManyField(Client, verbose_name='Клиенты рассылки', related_name='clients',
                                     help_text='Выберите клиентов для рассылки')
    message = models.ForeignKey(Message, verbose_name='Сообщение рассылки', on_delete=models.CASCADE,
                                help_text='Выберите сообщение для рассылки', related_name='messages')

    def __str__(self):
        return f'Рассылка от {self.created_at}'

    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'
        ordering = ('-created_at',)


class MailingLog(models.Model):
    mailing = models.ForeignKey(Mailing, verbose_name='Рассылка', on_delete=models.CASCADE, related_name='logs')
    sent_at = models.DateTimeField(auto_now_add=True, verbose_name='Время отправки рассылки',
                                   help_text='Укажите время отправки рассылки')
    is_success = models.BooleanField(default=False, verbose_name='Успешно',
                                     help_text='Укажите, успешно ли отправлена рассылка')
    server_response = models.TextField(verbose_name='Ответ сервера', **NULLABLE)

    def __str__(self):
        return f'Лог рассылки {self.mailing} (отправлен {self.sent_at})'

    class Meta:
        verbose_name = 'Лог рассылки'
        verbose_name_plural = 'Логи рассылок'
        ordering = ('-sent_at',)

