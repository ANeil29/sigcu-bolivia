from django.utils import timezone
from django.utils.deprecation import MiddlewareMixin


def get_ip(request):
    x_forwarded = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded:
        return x_forwarded.split(',')[0].strip()
    return request.META.get('REMOTE_ADDR')


class SesionActivaMiddleware(MiddlewareMixin):
    """Actualiza el último acceso del usuario cada vez que hace una petición."""

    def process_request(self, request):
        if request.user.is_authenticated:
            from .models import SesionActiva
            navegador = request.META.get('HTTP_USER_AGENT', '')[:200]
            SesionActiva.objects.update_or_create(
                usuario=request.user,
                defaults={
                    'ultimo_acceso': timezone.now(),
                    'ip':            get_ip(request),
                    'navegador':     navegador,
                }
            )


class AuditoriaMiddleware(MiddlewareMixin):
    """Registra automáticamente acciones POST (crear, editar, eliminar)."""

    # URLs que NO se registran (demasiado frecuentes o irrelevantes)
    EXCLUIR_PATHS = [
        '/static/', '/media/', '/favicon.ico',
        '/auth/token/', '/api/schema/',
    ]

    MAPA_ACCION = {
        'crear':    'CREAR',
        'editar':   'EDITAR',
        'eliminar': 'ELIMINAR',
        'exportar': 'EXPORTAR',
        'estado':   'EDITAR',
        'aprobar':  'EDITAR',
        'rechazar': 'ELIMINAR',
    }

    MAPA_MODULO = {
        'universidades': 'Universidades',
        'carreras':      'Carreras',
        'programas':     'Programas',
        'seguimiento':   'Seguimiento',
        'formularios':   'Formularios',
        'reportes':      'Reportes',
        'auth':          'Usuarios',
    }

    def process_response(self, request, response):
        if not request.user.is_authenticated:
            return response

        path = request.path
        if any(path.startswith(ex) for ex in self.EXCLUIR_PATHS):
            return response

        # Solo registrar POST exitosos (2xx o redirecciones 3xx)
        if request.method != 'POST':
            return response
        if response.status_code not in range(200, 400):
            return response

        from .models import RegistroActividad

        # Determinar módulo
        partes = path.strip('/').split('/')
        modulo = 'Sistema'
        for parte in partes:
            if parte in self.MAPA_MODULO:
                modulo = self.MAPA_MODULO[parte]
                break

        # Determinar acción
        accion = 'OTRO'
        for clave, valor in self.MAPA_ACCION.items():
            if clave in path:
                accion = valor
                break

        RegistroActividad.objects.create(
            usuario=request.user,
            accion=accion,
            modulo=modulo,
            descripcion=f'{request.method} {path}',
            ip=get_ip(request),
        )
        return response