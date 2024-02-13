from .base import *

DEBUG = True

# EMAILS conf

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Database

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

