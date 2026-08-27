from .settings import *
import os

DEBUG = False

ALLOWED_HOSTS = [
    'sigcu.uatf.edu.bo',
    'www.sigcu.uatf.edu.bo',
]

# Base de datos
DATABASES = {
    'default': {
        'ENGINE':   'django.db.backends.postgresql',
        'NAME':     os.environ.get('DB_NAME',     'sigcu_db'),
        'USER':     os.environ.get('DB_USER',     'sigcu_user'),
        'PASSWORD': os.environ.get('DB_PASSWORD', ''),
        'HOST':     os.environ.get('DB_HOST',     'localhost'),
        'PORT':     os.environ.get('DB_PORT',     '5432'),
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