from django.utils.timezone import datetime, now, timedelta


def get_reference_date() -> datetime:
    return now() - timedelta(days=10)
