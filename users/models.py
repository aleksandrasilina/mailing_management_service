from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django_countries.fields import CountryField


NULLABLE = {"blank": True, "null": True}


class User(AbstractUser):
    username = None

    email = models.EmailField(unique=True, verbose_name="Почта")
    first_name = models.CharField(
        max_length=150, verbose_name="Имя", **NULLABLE, help_text="Введите ваше имя"
    )
    last_name = models.CharField(
        max_length=150,
        verbose_name="Фамилия",
        **NULLABLE,
        help_text="Введите вашу фамилию",
    )
    phone_number = PhoneNumberField(
        verbose_name="Телефон",
        **NULLABLE,
        help_text="Введите номер телефона",
    )
    avatar = models.ImageField(
        upload_to="users/avatars/",
        verbose_name="Аватар",
        **NULLABLE,
        help_text="Загрузите свой аватар",
    )
    country = CountryField(
        verbose_name="Страна",
        **NULLABLE,
        help_text="Выберите страну",
        blank_label="(Выберите страну)",
    )
    token = models.CharField(max_length=100, verbose_name="Token", **NULLABLE)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.email})"

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
