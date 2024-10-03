from datetime import timedelta

import pytest
from django.contrib.auth import get_user_model
from django.utils import timezone

user = get_user_model()


@pytest.fixture
def create_register_today_user():
    return user.objects.create_user(
        username="test",
        password="test",
        email="test@test.com",
    )


@pytest.fixture
def create_register_not_today_user():
    return user.objects.create_user(
        username="test",
        password="test",
        email="test@test.com",
        date_joined=timezone.now() - timedelta(days=1),
    )
