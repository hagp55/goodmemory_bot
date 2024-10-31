from .base import *  # noqa
from .base import INSTALLED_APPS, MIDDLEWARE

ALLOWED_HOSTS = ["localhost", "0.0.0.0", "127.0.0.1"]

DEBUG = True

INSTALLED_APPS += [
    "django_extensions",
    "debug_toolbar",
]

MIDDLEWARE += [
    "debug_toolbar.middleware.DebugToolbarMiddleware",
]

INTERNAL_IPS = [
    "127.0.0.1",
]
