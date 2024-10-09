import pytest
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.fixture
@pytest.mark.django_db
def user():
    return User.objects.create_user(username="testuser", password="testpassword")
