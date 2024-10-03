import pytest
from django.conf import settings
from django.core.exceptions import ValidationError

from .models import Memory


@pytest.mark.django_db
def test_success_save_memory(create_register_not_today_user) -> None:
    assert Memory.objects.count() == 0
    Memory.objects.create(user=create_register_not_today_user, photo="example.jpg")
    assert Memory.objects.count() == 1


@pytest.mark.django_db
def test_success_save_memory_for_user_register_today(create_register_today_user):
    assert Memory.objects.count() == 0
    for _ in range(8):
        Memory.objects.create(user=create_register_today_user, photo="example.jpg")
    assert Memory.objects.count() == 8


@pytest.mark.django_db
def test_str_memories(create_register_not_today_user) -> None:
    memory = Memory.objects.create(user=create_register_not_today_user, photo="example.jpg")
    repr_mem = f"Фото {create_register_not_today_user.username } | загружено {memory.uploaded_at}"
    assert str(memory) == repr_mem


@pytest.mark.django_db
def test_not_success_save_memory_for_constraint_upload_1_photo_a_day(
    create_register_not_today_user,
) -> None:
    with pytest.raises(ValidationError, match="Разрешается загружать 1 фото в день"):
        for _ in range(2):
            Memory.objects.create(user=create_register_not_today_user, photo="example.jpg")


@pytest.mark.django_db
def test_not_success_save_memory_for_constraint_upload_10_photo_a_day(create_register_today_user):
    with pytest.raises(
        ValidationError,
        match=f"Разрешается загружать {settings.ALLOWED_NUMBER_PHOTO_PER_DAY} \
                    фотографий в день регистрации",
    ):
        for _ in range(11):
            Memory.objects.create(user=create_register_today_user, photo="example.jpg")
