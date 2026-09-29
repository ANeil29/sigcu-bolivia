from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from carreras.models import Carrera
from universidades.models import Universidad, Sede


@login_required
def dashboard(request):
    from seguimiento.models import ProcesoCurricular as PC

    carreras = Carrera.objects.select_related(
        'sede__facultad__universidad'
    ).prefetch_related('procesos').filter(en_funcionamiento=True)

    # Sedes únicas
    sedes_unicas = Sede.objects.filter(activa=True).values(
        'ciudad', 'facultad__universidad'
    ).distinct().count()

    # Conteo por tipo de proceso
    todos_ids    = set(carreras.values_list('id', flat=True))
    ids_rediseno = set(PC.objects.filter(tipo_proceso='REDISENO').values_list('carrera_id', flat=True))
    ids_diseno   = set(PC.objects.filter(tipo_proceso='DISENO').values_list('carrera_id', flat=True))
    ids_ajuste   = set(PC.objects.filter(tipo_proceso='AJUSTE').values_list('carrera_id', flat=True))
    ids_compl    = set(PC.objects.filter(tipo_proceso='COMPLEMENTACION').values_list('carrera_id', flat=True))
    ids_con_proceso = ids_rediseno | ids_diseno | ids_ajuste | ids_compl

    stats = {
        'total_carreras':       carreras.count(),
        'total_universidades':  Universidad.objects.filter(activa=True).count(),
        'total_sedes':          sedes_unicas,
        'vigentes':  sum(1 for c in carreras if c.estado_rediseno == 'VIGENTE'),
        'proximas':  sum(1 for c in carreras if c.estado_rediseno == 'PROXIMO'),
        'vencidas':  sum(1 for c in carreras if c.estado_rediseno == 'VENCIDO'),
        'sin_datos': sum(1 for c in carreras if c.estado_rediseno == 'SIN_DATOS'),
        # Procesos
        'con_rediseno':        len(ids_rediseno & todos_ids),
        'con_diseno':          len(ids_diseno & todos_ids),
        'con_ajuste':          len(ids_ajuste & todos_ids),
        'con_complementacion': len(ids_compl & todos_ids),
        'sin_proceso':         len(todos_ids - ids_con_proceso),
        'total_carreras_int':  len(todos_ids),
    }
    return render(request, 'core/dashboard.html', {'stats': stats})

@login_required
def mapa(request):
    return render(request, 'core/mapa.html')

def bienvenida_publica(request):
    """
    Primera pantalla que ve cualquier visitante.
    No requiere autenticación.
    Si ya está logueado lo manda directo al dashboard.
    """
    if request.user.is_authenticated:
        return redirect('bienvenida')
    return render(request, 'core/bienvenida_publica.html')


# Vista PRIVADA — requiere login, muestra stats
@login_required
def bienvenida(request):
    """
    Bienvenida personalizada después del login.
    Muestra estadísticas y botón al dashboard.
    """
    from universidades.models import Universidad, Sede
    from carreras.models import Carrera
    from seguimiento.models import ProcesoCurricular

    stats = {
        'total_carreras':      Carrera.objects.filter(en_funcionamiento=True).count(),
        'total_universidades': Universidad.objects.filter(activa=True).count(),
        'total_sedes':         Sede.objects.filter(activa=True).values(
                                   'ciudad', 'facultad__universidad'
                               ).distinct().count(),
        'total_procesos':      ProcesoCurricular.objects.count(),
    }
    return render(request, 'core/bienvenida.html', {'stats': stats})