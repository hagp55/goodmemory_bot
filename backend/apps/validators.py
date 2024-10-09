from django.core.exceptions import ValidationError


def is_validate_telegram_id(telegram_id: str) -> None:
    telegram_id = telegram_id if not telegram_id.startswith("-") else telegram_id[1:]
    if not telegram_id.isdigit():
        raise ValidationError(
            "%(value)s не корректный телеграм ID",
            params={"value": telegram_id},
        )
