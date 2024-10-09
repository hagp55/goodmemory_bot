from django.utils import timezone


def get_reference_date():
    return timezone.now() - timezone.timedelta(days=10)
