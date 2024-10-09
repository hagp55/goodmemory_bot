from django.core.exceptions import ValidationError


def is_valid_telegram_id(value: str) -> None:
    telegram_id = value if not value.startswith("-") else value[1:]
    if not telegram_id.isdigit():
        raise ValidationError(
            "%(value)s не корректный телеграм ID",
            params={"value": value},
        )
