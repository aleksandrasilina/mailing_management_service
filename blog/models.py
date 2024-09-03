from django.db import models

NULLABLE = {"blank": True, "null": True}


class Article(models.Model):
    title = models.CharField(
        max_length=150, verbose_name="Заголовок", help_text="Введите заголовок статьи"
    )
    content = models.TextField(
        verbose_name="Содержимое", help_text="Введите содержимое"
    )
    preview = models.ImageField(
        upload_to="blog/previews",
        verbose_name="Превью",
        help_text="Загрузите изображение для превью",
        null=True,
        blank=True,
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания",
        help_text="Укажите дату создания",
    )
    views_count = models.PositiveIntegerField(
        default=0,
        verbose_name="Количество просмотров",
        help_text="Укажите количество просмотров",
        editable=False
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Статья"
        verbose_name_plural = "Статьи"
        ordering = ["-created_at"]
