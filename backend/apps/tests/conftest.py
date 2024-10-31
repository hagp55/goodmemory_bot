import tempfile
from collections.abc import Generator

import pytest
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.test import override_settings

User = get_user_model()


@pytest.fixture
@pytest.mark.django_db
def user() -> Generator[AbstractUser, None, None]:
    yield User.objects.create_user(username="testuser", password="testpassword")


@pytest.fixture(scope="function")
def test_media_root() -> Generator[str, None, None]:
    with tempfile.TemporaryDirectory() as tmp_dir:
        with override_settings(MEDIA_ROOT=tmp_dir):
            yield tmp_dir
