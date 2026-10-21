from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from carreras.models import Carrera
from universidades.models import Universidad, Sede, Facultad
from django.db import models
from programas.models import Programa

@login_required
def dashboard(request):
    from universidades.models import Universidad, Sede, Facultad
    from carreras.models import Carrera
    from seguimiento.models import ProcesoCurricular as PC
    from django.utils import timezone

    anio_actual  = timezone.now().year
    # Por defecto muestra la gestión anterior
    anio_default = anio_actual - 1

    # Filtros desde GET
    filtro_facultad = request.GET.get('facultad', '')
    filtro_gestion  = request.GET.get('gestion',  str(anio_default))

    try:
        filtro_gestion_int = int(filtro_gestion)
    except (ValueError, TypeError):
        filtro_gestion_int = anio_default

    # Queryset base de carreras
    carreras_qs = Carrera.objects.prefetch_related('procesos').filter(
        en_funcionamiento=True
    )
    if filtro_facultad:
        carreras_qs = carreras_qs.filter(
            sede__facultad__id=filtro_facultad
        )

    # Procesos filtrados por gestión
    procesos_qs = PC.objects.filter(
        anio_inicio__lte=filtro_gestion_int
    ).filter(
        models.Q(anio_conclusion__gte=filtro_gestion_int) |
        models.Q(anio_conclusion__isnull=True)
    )
    if filtro_facultad:
        procesos_qs = procesos_qs.filter(
            carrera__sede__facultad__id=filtro_facultad
        )

    todos_ids    = set(carreras_qs.values_list('id', flat=True))
    ids_rediseno = set(PC.objects.filter(
        tipo_proceso='REDISENO').values_list('carrera_id', flat=True))
    ids_diseno   = set(PC.objects.filter(
        tipo_proceso='DISENO').values_list('carrera_id', flat=True))
    ids_ajuste   = set(PC.objects.filter(
        tipo_proceso='AJUSTE').values_list('carrera_id', flat=True))
    ids_compl    = set(PC.objects.filter(
        tipo_proceso='COMPLEMENTACION').values_list('carrera_id', flat=True))
    ids_con      = ids_rediseno | ids_diseno | ids_ajuste | ids_compl
    total_int    = len(todos_ids) or 1

    # Estado de procesos en la gestión filtrada
    procesos_concluidos  = procesos_qs.filter(estado='CONCLUIDO').count()
    procesos_en_proceso  = procesos_qs.filter(estado='EN_PROCESO').count()
    procesos_archivados  = procesos_qs.filter(estado='ARCHIVADO').count()
    total_procesos_gestion = procesos_qs.count()

    # Por tipo en la gestión
    redisenos_gestion = procesos_qs.filter(tipo_proceso='REDISENO')
    disenos_gestion   = procesos_qs.filter(tipo_proceso='DISENO')
    ajustes_gestion   = procesos_qs.filter(tipo_proceso='AJUSTE')

    # Facultades para el filtro
    facultades = Facultad.objects.select_related('universidad').order_by(
        'universidad__sigla', 'nombre'
    )

    # Años disponibles para el filtro de gestión
    anios_disponibles = list(range(anio_actual, 2009, -1))

    stats = {
        'total_universidades':  Universidad.objects.filter(activa=True).count(),
        'total_facultades': Facultad.objects.filter(universidad__activa=True).count(),
        'total_carreras':       carreras_qs.count(),
        'total_programas': Programa.objects.filter(activo=True).count(),
        'total_sedes':          Sede.objects.filter(activa=True).values(
                                    'ciudad', 'facultad__universidad'
                                ).distinct().count(),
        'total_procesos':       total_procesos_gestion,
        'vigentes':  sum(1 for c in carreras_qs if c.estado_rediseno == 'VIGENTE'),
        'proximas':  sum(1 for c in carreras_qs if c.estado_rediseno == 'PROXIMO'),
        'vencidas':  sum(1 for c in carreras_qs if c.estado_rediseno == 'VENCIDO'),
        'sin_datos': sum(1 for c in carreras_qs if c.estado_rediseno == 'SIN_DATOS'),
        'con_rediseno':        len(ids_rediseno & todos_ids),
        'con_diseno':          len(ids_diseno & todos_ids),
        'con_ajuste':          len(ids_ajuste & todos_ids),
        'con_complementacion': len(ids_compl & todos_ids),
        'sin_proceso':         len(todos_ids - ids_con),
        'total_carreras_int':  len(todos_ids),
        'pct_rediseno':        round(len(ids_rediseno & todos_ids) / total_int * 100),
        'pct_diseno':          round(len(ids_diseno & todos_ids)   / total_int * 100),
        'pct_ajuste':          round(len(ids_ajuste & todos_ids)   / total_int * 100),
        'pct_complementacion': round(len(ids_compl & todos_ids)    / total_int * 100),
        'pct_sin_proceso':     round(len(todos_ids - ids_con)      / total_int * 100),
        # Estado procesos en gestión
        'procesos_concluidos':  procesos_concluidos,
        'procesos_en_proceso':  procesos_en_proceso,
        'procesos_archivados':  procesos_archivados,
        'total_procesos_gestion': total_procesos_gestion,
        'redisenos_concluidos': redisenos_gestion.filter(estado='CONCLUIDO').count(),
        'redisenos_en_proceso': redisenos_gestion.filter(estado='EN_PROCESO').count(),
        'disenos_concluidos':   disenos_gestion.filter(estado='CONCLUIDO').count(),
        'disenos_en_proceso':   disenos_gestion.filter(estado='EN_PROCESO').count(),
        'ajustes_concluidos':   ajustes_gestion.filter(estado='CONCLUIDO').count(),
        'ajustes_en_proceso':   ajustes_gestion.filter(estado='EN_PROCESO').count(),
    }

    return render(request, 'core/dashboard.html', {
        'stats':             stats,
        'facultades':        facultades,
        'filtro_facultad':   filtro_facultad,
        'filtro_gestion':    filtro_gestion,
        'filtro_gestion_int': filtro_gestion_int,
        'anios_disponibles': anios_disponibles,
        'anio_default':      anio_default,
    })

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
    from universidades.models import Universidad, Sede
    from carreras.models import Carrera
    from seguimiento.models import ProcesoCurricular as PC

    carreras = Carrera.objects.prefetch_related('procesos').filter(
        en_funcionamiento=True)

    todos_ids    = set(carreras.values_list('id', flat=True))
    ids_rediseno = set(PC.objects.filter(tipo_proceso='REDISENO'
                       ).values_list('carrera_id', flat=True))
    ids_diseno   = set(PC.objects.filter(tipo_proceso='DISENO'
                       ).values_list('carrera_id', flat=True))
    ids_ajuste   = set(PC.objects.filter(tipo_proceso='AJUSTE'
                       ).values_list('carrera_id', flat=True))
    ids_compl    = set(PC.objects.filter(tipo_proceso='COMPLEMENTACION'
                       ).values_list('carrera_id', flat=True))
    ids_con      = ids_rediseno | ids_diseno | ids_ajuste | ids_compl
    total_int    = len(todos_ids) or 1

    stats = {
        'total_carreras':       carreras.count(),
        'total_universidades':  Universidad.objects.filter(activa=True).count(),
        'total_sedes':          Sede.objects.filter(activa=True).values(
                                    'ciudad', 'facultad__universidad'
                                ).distinct().count(),
        'total_procesos':       PC.objects.count(),
        'vigentes':  sum(1 for c in carreras if c.estado_rediseno == 'VIGENTE'),
        'proximas':  sum(1 for c in carreras if c.estado_rediseno == 'PROXIMO'),
        'vencidas':  sum(1 for c in carreras if c.estado_rediseno == 'VENCIDO'),
        'sin_datos': sum(1 for c in carreras if c.estado_rediseno == 'SIN_DATOS'),
        'con_rediseno':        len(ids_rediseno & todos_ids),
        'con_diseno':          len(ids_diseno & todos_ids),
        'con_ajuste':          len(ids_ajuste & todos_ids),
        'con_complementacion': len(ids_compl & todos_ids),
        'sin_proceso':         len(todos_ids - ids_con),
        'total_carreras_int':  len(todos_ids),
        'pct_rediseno':        round(len(ids_rediseno & todos_ids) / total_int * 100),
        'pct_diseno':          round(len(ids_diseno & todos_ids)   / total_int * 100),
        'pct_ajuste':          round(len(ids_ajuste & todos_ids)   / total_int * 100),
        'pct_complementacion': round(len(ids_compl & todos_ids)    / total_int * 100),
        'pct_sin_proceso':     round(len(todos_ids - ids_con)      / total_int * 100),
    }
    return render(request, 'core/bienvenida.html', {'stats': stats})