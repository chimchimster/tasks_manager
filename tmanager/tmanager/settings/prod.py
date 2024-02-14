from .base import *

DEBUG = False

# EMAIL configuration

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.getenv('EMAIL_HOST')
EMAIL_PORT = os.getenv('EMAIL_PORT')
EMAIL_HOST_USER = os.getenv('EMAIL_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_PASSWORD')
EMAIL_USE_TLS = True

# REST FRAMEWORK configuration

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ],
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.JSONParser',
    ],
}

# Database

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('POSTGRESQL_DB'),
        'USER': os.getenv('POSTGRESQL_USER'),
        'PASSWORD': os.getenv('POSTGRESQL_PWD'),
        'HOST': os.getenv('POSTGRESQL_HOST'),
        'PORT': os.getenv('POSTGRESQL_PORT'),
    }
}


ALLOWED_HOSTS = ['*']