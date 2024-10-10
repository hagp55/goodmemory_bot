import pytest
from django.core.exceptions import ValidationError

from apps.validators import is_validate_telegram_id


def test_is_validate_telegram_id() -> None:
    assert is_validate_telegram_id("234545453534") is None
    assert is_validate_telegram_id("-234545453534") is None


@pytest.mark.parametrize(
    "telegram_id",
    ["test", "-test123"],
)
def test_is_not_validate_telegram_id(telegram_id) -> None:
    with pytest.raises(ValidationError, match=f"{telegram_id} не корректный телеграм ID"):
        is_validate_telegram_id(telegram_id)
