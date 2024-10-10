from django.core.exceptions import ValidationError


def is_validate_telegram_id(value: str) -> None:
    """
    Validates a telegram ID.

    Args:
        value (str): The telegram ID to validate.

    Raises:
        ValidationError: If the telegram ID is not a digit or starts with a minus sign.
    """
    telegram_id = value if not value.startswith("-") else value[1:]
    if not telegram_id.isdigit():
        raise ValidationError(
            "%(value)s не корректный телеграм ID",
            params={"value": value},
        )
