from django.core.exceptions import ValidationError


def is_validate_telegram_id(telegram_id: str):
    if telegram_id.startswith("-"):
        telegram_id = telegram_id[1:]
    if not telegram_id.isdigit():
        raise ValidationError(
            "%(value)s не корректный телеграм ID",
            params={"value": telegram_id},
        )
