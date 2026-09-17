from .settings import *
import os

DEBUG = False

ALLOWED_HOSTS = [
    'sigcu.uatf.edu.bo',
    'www.sigcu.uatf.edu.bo',
]

# Encoding
DEFAULT_CHARSET = 'utf-8'
FILE_CHARSET    = 'utf-8'

# Base de datos
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST'),
        'PORT': config('DB_PORT'),
        'OPTIONS': {
            'client_encoding': 'UTF8',
        },
    }
}

STATIC_URL  = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
MEDIA_URL   = '/media/'
MEDIA_ROOT  = BASE_DIR / 'media'

# Seguridad HTTPS
CSRF_COOKIE_SECURE    = True
SESSION_COOKIE_SECURE = True
SECURE_SSL_REDIRECT   = True
SECURE_HSTS_SECONDS   = 31536000

# Logs en producción
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': BASE_DIR / 'logs/django_errors.log',
        },
    },
    'root': {
        'handlers': ['file'],
        'level': 'ERROR',
    },
}