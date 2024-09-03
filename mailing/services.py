import smtplib
import datetime
from time import sleep

import pytz
from apscheduler.schedulers.background import BackgroundScheduler
from django.core.mail import send_mail

from config import settings
from mailing.models import Mailing, MailingLog


def send_mailing():
    """Функция для рассылки клиентам"""

    zone = pytz.timezone(settings.TIME_ZONE)
    current_datetime = datetime.datetime.now(zone)

    mailings = Mailing.objects.all()

    for mailing in mailings:
        # проверяем не наступил ли срок окончания рассылки
        if mailing.last_send_time:
            if mailing.last_send_time <= current_datetime:
                mailing.mailing_status = 'COMPLETED'
                mailing.save()

        # проверяем закончился ли период между рассылками
        mailing_log = MailingLog.objects.filter(mailing=mailing).order_by('-sent_at').first()
        if mailing_log:
            time_delta = current_datetime - mailing_log.sent_at

            if mailing.periodicity == "DAILY" and time_delta.days >= 1:
                mailing.next_send_time = mailing_log.sent_at + datetime.timedelta(days=1)
                mailing.mailing_status = 'LAUNCHED'
                mailing.save()
            if mailing.periodicity == "WEEKLY" and time_delta.days >= 7:
                mailing.next_send_time = mailing_log.sent_at + datetime.timedelta(days=7)
                mailing.mailing_status = 'LAUNCHED'
                mailing.save()
            if mailing.periodicity == "MONTHLY" and time_delta.days >= 30:
                mailing.next_send_time = mailing_log.sent_at + datetime.timedelta(days=30)
                mailing.mailing_status = 'LAUNCHED'
                mailing.save()

    mailings = Mailing.objects.filter(first_send_time__lte=current_datetime).filter(
        mailing_status__in=['CREATED', 'LAUNCHED'])

    if not mailings.exists():
        print("Нет рассылок готовых к отправке")

    for mailing in mailings:
        try:
            server_response = send_mail(
                subject=mailing.message.title,
                message=mailing.message.body,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[client.email for client in mailing.clients.all()] + [settings.EMAIL_HOST_USER],
                fail_silently=False
            )
            mailing.mailing_status = 'PAUSED'
            mailing.save()

            MailingLog.objects.create(mailing=mailing, is_success=True, server_response=server_response,
                                      owner=mailing.owner)
            print(f"Рассылка {mailing} успешно отправлена")

        except smtplib.SMTPException as e:
            MailingLog.objects.create(mailing=mailing, is_success=False, server_response=e, owner=mailing.owner)
            print(f"Ошибка при отправке рассылки {mailing}")


def start_mailing():
    """Запускает рассылки клиентам"""

    scheduler = BackgroundScheduler()
    scheduler.add_job(send_mailing, 'interval', seconds=10)
    scheduler.start()

    while True:
        sleep(1)
