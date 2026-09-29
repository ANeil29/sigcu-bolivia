"""
WSGI config for config project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os
import sys

os.environ.setdefault('PYTHONIOENCODING', 'utf-8')
os.environ.setdefault('LANG', 'C.UTF-8')
os.environ.setdefault('LC_ALL', 'C.UTF-8')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings_servidor')

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
