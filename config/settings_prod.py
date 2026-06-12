# config/settings_prod.py
from .settings import *

DEBUG = False

ALLOWED_HOSTS = ['alvin2907.pythonanywhere.com']

# Base de datos en producción — SQLite es suficiente para PythonAnywhere gratuito
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db_sigcu.sqlite3',
    }
}

# Archivos estáticos
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Seguridad
CSRF_COOKIE_SECURE   = False  # True cuando tengas HTTPS propio
SESSION_COOKIE_SECURE = False