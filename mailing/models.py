from django.db import models

from users.models import User

NULLABLE = {"blank": True, "null": True}
PERIODICITY_CHOICES = (
    (
        "DAILY",
        "раз в день",
    ),
    (
        "WEEKLY",
        "раз в неделю",
    ),
    (
        "MONTHLY",
        "раз в месяц",
    ),
)
MAILING_STATUS_CHOICES = (
    (
        "CREATED",
        "создана",
    ),
    (
        "LAUNCHED",
        "запущена",
    ),
    (
        "PAUSED",
        "в ожидании отправки",
    ),
    (
        "COMPLETED",
        "завершена",
    ),
)


class Client(models.Model):
    first_name = models.CharField(
        max_length=100, verbose_name="Имя", help_text="Введите имя клиента"
    )
    last_name = models.CharField(
        max_length=150, verbose_name="Фамилия", help_text="Введите фамилию клиента"
    )
    email = models.EmailField(
        verbose_name="Почта", unique=True, help_text="Введите электронную почту клиента"
    )
    avatar = models.ImageField(
        upload_to="mailing/avatars/",
        verbose_name="Аватар",
        **NULLABLE,
        help_text="Загрузите аватар клиента",
    )
    comment = models.TextField(
        verbose_name="Комментарий", **NULLABLE, help_text="Введите комментарий"
    )
    owner = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        **NULLABLE,
        verbose_name="Владелец",
    )

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.email})"

    class Meta:
        verbose_name = "Клиент"
        verbose_name_plural = "Клиенты"
        ordering = ("owner", "last_name",)


class Message(models.Model):
    title = models.CharField(
        max_length=200,
        verbose_name="Тема сообщения",
        help_text="Напишите тему сообщения",
    )
    body = models.TextField(
        verbose_name="Содержание сообщения", help_text="Напишите сообщение"
    )
    owner = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        **NULLABLE,
        verbose_name="Владелец",
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщения"
        ordering = ("owner", "title",)


class Mailing(models.Model):
    message = models.ForeignKey(
        Message,
        verbose_name="Сообщение рассылки",
        on_delete=models.CASCADE,
        help_text="Выберите сообщение для рассылки",
        related_name="mailings",
    )
    first_send_time = models.DateTimeField(
        verbose_name="Дата и время начала рассылки",
        help_text="Введите дату и время начала рассылки",
        **NULLABLE,
    )
    next_send_time = models.DateTimeField(
        verbose_name="Дата и время следующей отправки рассылки",
        **NULLABLE,
        editable=False,
    )
    last_send_time = models.DateTimeField(
        verbose_name="Дата и время окончания рассылки",
        help_text="Введите дату и время окончания рассылки",
        **NULLABLE,
    )
    periodicity = models.CharField(
        max_length=20,
        verbose_name="Периодичность рассылки",
        help_text="Выберите периодичность рассылки",
        choices=PERIODICITY_CHOICES,
    )
    mailing_status = models.CharField(
        max_length=100,
        verbose_name="Статус рассылки",
        help_text="Выберите статус рассылки",
        choices=MAILING_STATUS_CHOICES,
        default="created",
    )
    clients = models.ManyToManyField(
        Client,
        verbose_name="Клиенты рассылки",
        help_text="Выберите клиентов для рассылки",
        related_name="mailings",
    )
    owner = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        **NULLABLE,
        verbose_name="Владелец",
    )

    def __str__(self):
        return f'Рассылка "{self.message}" от {self.first_send_time.strftime("%d.%m.%Y %H:%M")}'

    class Meta:
        verbose_name = "Рассылка"
        verbose_name_plural = "Рассылки"
        ordering = ("-first_send_time",)
        permissions = [
            ("can_change_mailing_status", "Can change mailing status"),
        ]


class MailingLog(models.Model):
    mailing = models.ForeignKey(
        Mailing, verbose_name="Рассылка", on_delete=models.CASCADE, related_name="logs"
    )
    sent_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Время отправки рассылки",
    )
    is_success = models.BooleanField(
        default=False,
        verbose_name="Статус попытки рассылки",
        editable=False
    )
    server_response = models.TextField(verbose_name="Ответ сервера", **NULLABLE)
    owner = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        **NULLABLE,
        verbose_name="Владелец",
    )

    def __str__(self):
        return f"Попытка рассылки: {self.mailing}, отправлена {self.sent_at.strftime("%d.%m.%Y %H:%M")}"

    class Meta:
        verbose_name = "Лог рассылки"
        verbose_name_plural = "Логи рассылок"
        ordering = ("-sent_at",)
