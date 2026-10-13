import base64
import os
from django.conf import settings


def logo_base64(nombre_archivo):
    """Convierte un logo estático a base64 para incrustarlo en PDF."""
    ruta = os.path.join(settings.BASE_DIR, 'static', 'img', nombre_archivo)
    if not os.path.isfile(ruta):
        # Intenta en staticfiles
        ruta = os.path.join(settings.BASE_DIR, 'staticfiles', 'img', nombre_archivo)
    if not os.path.isfile(ruta):
        return ''
    with open(ruta, 'rb') as f:
        datos = base64.b64encode(f.read()).decode('utf-8')
    ext = nombre_archivo.split('.')[-1].lower()
    mime = 'image/jpeg' if ext in ('jpg', 'jpeg') else f'image/{ext}'
    return f'data:{mime};base64,{datos}'