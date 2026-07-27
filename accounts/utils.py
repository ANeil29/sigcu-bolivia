from .models import RegistroActividad


def registrar_actividad(request, accion, modulo, descripcion='',
                         objeto_id=None, objeto_repr=''):
    """
    Helper para registrar manualmente una actividad importante.
    Uso: registrar_actividad(request, 'CREAR', 'Carreras', 'Nueva carrera: Derecho')
    """
    from accounts.middleware import get_ip

    if not request.user.is_authenticated:
        return

    RegistroActividad.objects.create(
        usuario=request.user,
        accion=accion,
        modulo=modulo,
        descripcion=descripcion,
        ip=get_ip(request),
        objeto_id=objeto_id,
        objeto_repr=objeto_repr,
    )