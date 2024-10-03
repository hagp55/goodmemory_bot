from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    class Meta:
        verbose_name = "Пользователя"
        verbose_name_plural = "Пользователи"
