from django.contrib import admin
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

from apps.services.prepare_date import get_reference_date
from apps.validators import is_validate_telegram_id


class User(AbstractUser):
    telegram_id = models.CharField(
        max_length=20,
        verbose_name="Телеграм ID",
        validators=[is_validate_telegram_id],
        help_text="формат телеграм ID: 1234567890 или -1234567890",
    )
    reference_date = models.DateTimeField(
        default=get_reference_date,
        verbose_name="Дата отсчёта",
    )

    class Meta:
        verbose_name = "Пользователя"
        verbose_name_plural = "Пользователи"

    @property
    @admin.display(description="Количество загруженных воспоминаний")
    def total_uploaded_memories(self) -> int:
        return self.memories.all().count()

    @property
    @admin.display(description="Количество доступных для загрузки воспоминаний")
    def number_memories_available_for_upload(self) -> int:
        return (
            (timezone.now().date() - self.reference_date.date()).days
        ) - self.total_uploaded_memories


class Memory(models.Model):
    photo = models.ImageField(upload_to="", verbose_name="Фотография")
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Пользователь",
        related_name="memories",
    )
    uploaded_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата загрузки",
    )

    class Meta:
        verbose_name = "Воспоминание"
        verbose_name_plural = "Воспоминания"
        ordering = ("-uploaded_at",)

    def __str__(self) -> str:
        return f"Воспоминание {self.pk} | загружено {self.uploaded_at}"
