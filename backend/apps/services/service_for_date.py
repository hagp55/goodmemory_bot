from django.utils.timezone import datetime, now, timedelta


def get_reference_date() -> datetime:
    """
    Returns the reference date, which is the current date minus 10 days.

    Returns:
        datetime: The reference date.
    """
    return now() - timedelta(days=10)
