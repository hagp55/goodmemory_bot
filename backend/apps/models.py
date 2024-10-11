from pathlib import Path

from django.contrib import admin
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator
from django.db import models
from django.utils.timezone import now

from apps.services.service_for_date import get_reference_date
from apps.validators import is_validate_telegram_id


class User(AbstractUser):
    """
    A model representing a user with a telegram ID and a reference date.

    Attributes:
        telegram_id (models.CharField): The telegram ID of the user.
        reference_date (models.DateTimeField): The reference date for the user.
        other fields are default User.

    Meta:
        verbose_name (str): The singular name for the model.
        verbose_name_plural (str): The plural name for the model.

    Methods:
        total_uploaded_photos: Returns the total number of uploaded photos for the user.
        number_photos_available_for_upload: Returns the number of photos available
        for upload for the user.
    """

    telegram_id = models.CharField(
        max_length=20,
        blank=True,
        verbose_name="Телеграм ID",
        validators=[
            is_validate_telegram_id,
            MinLengthValidator(7),
        ],
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
    @admin.display(description="Количество загруженных фотографий")
    def total_uploaded_photos(self) -> int:
        """
        Returns the total number of uploaded photos for the user.

        Returns:
            int: The total number of uploaded photos for the user.
        """
        return self.photos.all().count()

    @property
    @admin.display(description="Количество доступных для загрузки фотографий")
    def number_photos_available_for_upload(self) -> int:
        """
        Returns the number of photos available for upload for the user.

        Returns:
            int: The number of photos available for upload for the user.
        """
        return ((now().date() - self.reference_date.date()).days) - self.total_uploaded_photos


class Photo(models.Model):
    """
    A model representing a photo with an associated photo file, user, and upload date.

    Attributes:
        photo (models.ImageField): The photo file associated with the photo.
        user (models.ForeignKey): The user who uploaded the photo.
        uploaded_at (models.DateTimeField): The date and time when the photo was uploaded.

    Meta:
        verbose_name (str): The singular name for the model.
        verbose_name_plural (str): The plural name for the model.
        ordering (tuple): The field to use when ordering the query set.

    Methods:
        __str__: Returns a string representation of the photo.
        clean: Validates the photo before saving.
        save: Saves the photo to the database.
        delete: Deletes the photo from the database and
        removes the associated photo file if it exists.
    """

    photo = models.ImageField(upload_to="%Y/%m", verbose_name="Фотография")
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Пользователь",
        related_name="photos",
    )
    uploaded_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата загрузки",
    )

    class Meta:
        verbose_name = "Фотографию"
        verbose_name_plural = "Фотографии"
        ordering = ("-uploaded_at",)

    def __str__(self) -> str:
        return f"фотография id: {self.pk} | загружено {self.uploaded_at.date()}"

    def clean(self) -> None:
        """
        Validates the photo before saving.

        Raises:
            ValidationError: If the user has no photos available for upload.
        """
        if not bool(self.user.number_photos_available_for_upload):
            raise ValidationError("Ваш лимит исчерпан, попробуйте завтра")

    def save(self, *args, **kwargs) -> None:
        """
        Saves the photo to the database.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
        """
        self.full_clean()
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs) -> None:
        """
        Deletes the photo from the database and removes the associated photo file if it exists.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
        """
        photo_path = Path(self.photo.path)
        super().delete(*args, **kwargs)

        if photo_path.exists() and photo_path.is_file():
            photo_path.unlink()
