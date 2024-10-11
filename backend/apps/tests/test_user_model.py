import pytest
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.utils.timezone import timedelta

User = get_user_model()


@pytest.mark.django_db
def test_success_create_user(user) -> None:
    assert User.objects.count() == 1
    assert str(user) == user.username
    assert user.total_uploaded_photos == 0
    assert user.number_photos_available_for_upload == 10
    assert user.reference_date.date() == user.date_joined.date() - timedelta(days=10)


@pytest.mark.django_db
def test_not_success_create_user_with_no_valid_telegram_id() -> None:
    assert User.objects.count() == 0
    with pytest.raises(ValidationError):
        user = User(username="test", password="test", telegram_id="aa56453554")
        user.full_clean()
        user.save()
    assert User.objects.count() == 0
