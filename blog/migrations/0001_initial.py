# Generated by Django 4.2.2 on 2024-09-01 12:18

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Article",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "title",
                    models.CharField(
                        help_text="Введите заголовок статьи",
                        max_length=150,
                        verbose_name="Заголовок",
                    ),
                ),
                (
                    "content",
                    models.TextField(
                        help_text="Введите содержимое", verbose_name="Содержимое"
                    ),
                ),
                (
                    "preview",
                    models.ImageField(
                        blank=True,
                        help_text="Загрузите изображение для превью",
                        null=True,
                        upload_to="blog/previews",
                        verbose_name="Превью",
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(
                        auto_now_add=True,
                        help_text="Укажите дату создания",
                        verbose_name="Дата создания",
                    ),
                ),
                (
                    "views_count",
                    models.PositiveIntegerField(
                        default=0,
                        editable=False,
                        help_text="Укажите количество просмотров",
                        verbose_name="Количество просмотров",
                    ),
                ),
            ],
            options={
                "verbose_name": "Статья",
                "verbose_name_plural": "Статьи",
                "ordering": ["-created_at"],
            },
        ),
    ]
