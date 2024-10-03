import os

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone

user = get_user_model()


class Memory(models.Model):
    photo = models.ImageField(upload_to="", verbose_name="Фотография")
    user = models.ForeignKey(
        user,
        on_delete=models.CASCADE,
        verbose_name="Пользователь",
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
        return f"Фото {self.user.username } | загружено {self.uploaded_at}"

    def clean(self) -> None:
        today = timezone.now().date()
        register_user_date = self.user.date_joined.date()
        if (
            Memory.objects.filter(uploaded_at__date=register_user_date).count()
            >= settings.ALLOWED_NUMBER_PHOTO_PER_DAY
        ):
            raise ValidationError(
                f"Разрешается загружать {settings.ALLOWED_NUMBER_PHOTO_PER_DAY} \
                    фотографий в день регистрации"
            )
        if Memory.objects.filter(uploaded_at__date=today).count() >= 1 and (
            today != register_user_date
        ):
            raise ValidationError("Разрешается загружать 1 фото в день")

    def save(self, *args, **kwargs) -> None:
        self.full_clean()
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs) -> None:
        photo_path = self.photo.path if self.photo else None
        print(photo_path)
        self.is_being_deleted = True
        super().delete(*args, **kwargs)
        if photo_path and os.path.isfile(photo_path):
            os.remove(photo_path)
