from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template.loader import render_to_string
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment
from carreras.models import Carrera
from programas.models import Programa
from universidades.models import Universidad, Sede
from seguimiento.models import ProcesoCurricular
from formularios.models import FormularioValoracion


@login_required
def vista_estadisticas(request):
    """Vista HTML del resumen estadístico con gráficas."""
    carreras = Carrera.objects.prefetch_related('procesos').filter(en_funcionamiento=True)
    programas = Programa.objects.filter(activo=True)
    procesos  = ProcesoCurricular.objects.all()

    # Por departamento
    from django.db.models import Count
    sedes_por_depto = Sede.objects.filter(activa=True).values(
        'departamento', 'ciudad', 'facultad__universidad'
    ).distinct().values(
        'departamento'
    ).annotate(total=Count('ciudad', distinct=True)).order_by('departamento')

    carreras_por_universidad = Carrera.objects.filter(
        en_funcionamiento=True
    ).values(
        'sede__facultad__universidad__sigla'
    ).annotate(total=Count('id')).order_by('-total')[:10]

    programas_por_estado = {
        'FORMULACION':   programas.filter(estado='FORMULACION').count(),
        'APROBACION':    programas.filter(estado='APROBACION').count(),
        'IMPLEMENTACION': programas.filter(estado='IMPLEMENTACION').count(),
        'SUSPENDIDO':    programas.filter(estado='SUSPENDIDO').count(),
    }

    stats = {
        'total_carreras':      carreras.count(),
        'total_programas':     programas.count(),
        'total_universidades': Universidad.objects.filter(activa=True).count(),
        'total_sedes': Sede.objects.filter(activa=True).values('ciudad', 'facultad__universidad').distinct().count(),
        'total_procesos':      procesos.count(),
        'procesos_en_proceso': procesos.filter(estado='EN_PROCESO').count(),
        'procesos_concluidos': procesos.filter(estado='CONCLUIDO').count(),
        'formularios_total':   FormularioValoracion.objects.count(),
        'formularios_aprobados': FormularioValoracion.objects.filter(estado='APROBADO').count(),
        # Estado rediseño
        'vigentes':  sum(1 for c in carreras if c.estado_rediseno == 'VIGENTE'),
        'proximas':  sum(1 for c in carreras if c.estado_rediseno == 'PROXIMO'),
        'vencidas':  sum(1 for c in carreras if c.estado_rediseno == 'VENCIDO'),
        'sin_datos': sum(1 for c in carreras if c.estado_rediseno == 'SIN_DATOS'),
    }

    return render(request, 'reportes/estadisticas.html', {
        'stats':                   stats,
        'sedes_por_depto':         list(sedes_por_depto),
        'carreras_por_universidad': list(carreras_por_universidad),
        'programas_por_estado':    programas_por_estado,
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def resumen_estadisticas(request):
    """Endpoint JSON para consumir desde JS o apps externas."""
    carreras = Carrera.objects.prefetch_related('procesos').filter(en_funcionamiento=True)
    return Response({
        'total_carreras':      carreras.count(),
        'total_universidades': Universidad.objects.filter(activa=True).count(),
        'total_sedes': Sede.objects.filter(activa=True).values('ciudad', 'facultad__universidad').distinct().count(),
        'vigentes':  sum(1 for c in carreras if c.estado_rediseno == 'VIGENTE'),
        'proximas':  sum(1 for c in carreras if c.estado_rediseno == 'PROXIMO'),
        'vencidas':  sum(1 for c in carreras if c.estado_rediseno == 'VENCIDO'),
        'sin_datos': sum(1 for c in carreras if c.estado_rediseno == 'SIN_DATOS'),
    })


@login_required
def exportar_carreras_excel(request):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = 'Carreras SIGCU'

    headers = ['N°', 'Universidad', 'Facultad', 'Sede', 'Ciudad',
               'Carrera', 'Grado', 'Tipo', 'Funcionando', 'Estado Rediseño']
    for col, h in enumerate(headers, 1):
        cell           = ws.cell(row=1, column=col, value=h)
        cell.font      = Font(bold=True, color='FFFFFF')
        cell.fill      = PatternFill('solid', fgColor='0F1F3D')
        cell.alignment = Alignment(horizontal='center')

    carreras = Carrera.objects.select_related(
        'sede__facultad__universidad'
    ).prefetch_related('procesos').filter(en_funcionamiento=True).order_by(
        'sede__facultad__universidad__sigla', 'nombre'
    )
    for i, c in enumerate(carreras, 2):
        ws.cell(row=i, column=1,  value=i - 1)
        ws.cell(row=i, column=2,  value=c.sede.facultad.universidad.sigla)
        ws.cell(row=i, column=3,  value=c.sede.facultad.nombre)
        ws.cell(row=i, column=4,  value=c.sede.nombre)
        ws.cell(row=i, column=5,  value=c.sede.ciudad)
        ws.cell(row=i, column=6,  value=c.nombre)
        ws.cell(row=i, column=7,  value=c.get_grado_display())
        ws.cell(row=i, column=8,  value=c.get_tipo_display())
        ws.cell(row=i, column=9,  value='Sí' if c.en_funcionamiento else 'No')
        ws.cell(row=i, column=10, value=c.estado_rediseno)

    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename=carreras_sigcu.xlsx'
    wb.save(response)
    return response

@login_required
def exportar_estadisticas_pdf(request):
    from xhtml2pdf import pisa
    from io import BytesIO
    from django.db.models import Count
    from django.utils import timezone
    from seguimiento.models import ProcesoCurricular as PC

    carreras  = Carrera.objects.prefetch_related('procesos').filter(en_funcionamiento=True)
    programas = Programa.objects.filter(activo=True)
    procesos  = ProcesoCurricular.objects.all()

    sedes_unicas = Sede.objects.filter(activa=True).values(
        'ciudad', 'facultad__universidad'
    ).distinct().count()

    sedes_por_depto = list(
        Sede.objects.filter(activa=True).values(
            'departamento', 'ciudad', 'facultad__universidad'
        ).distinct().values('departamento').annotate(
            total=Count('ciudad', distinct=True)
        ).order_by('departamento')
    )

    carreras_por_universidad = list(
        Carrera.objects.filter(en_funcionamiento=True).values(
            'sede__facultad__universidad__sigla',
            'sede__facultad__universidad__nombre',
        ).annotate(total=Count('id')).order_by('-total')
    )

    todos_ids    = set(carreras.values_list('id', flat=True))
    ids_rediseno = set(PC.objects.filter(tipo_proceso='REDISENO').values_list('carrera_id', flat=True))
    ids_diseno   = set(PC.objects.filter(tipo_proceso='DISENO').values_list('carrera_id', flat=True))
    ids_ajuste   = set(PC.objects.filter(tipo_proceso='AJUSTE').values_list('carrera_id', flat=True))
    ids_compl    = set(PC.objects.filter(tipo_proceso='COMPLEMENTACION').values_list('carrera_id', flat=True))
    ids_con_proceso = ids_rediseno | ids_diseno | ids_ajuste | ids_compl

    total_int = len(todos_ids) or 1  # evitar división por cero

    stats = {
        'total_carreras':       carreras.count(),
        'total_programas':      programas.count(),
        'total_universidades':  Universidad.objects.filter(activa=True).count(),
        'total_sedes':          sedes_unicas,
        'total_procesos':       procesos.count(),
        'procesos_en_proceso':  procesos.filter(estado='EN_PROCESO').count(),
        'procesos_concluidos':  procesos.filter(estado='CONCLUIDO').count(),
        'formularios_total':    FormularioValoracion.objects.count(),
        'formularios_aprobados': FormularioValoracion.objects.filter(estado='APROBADO').count(),
        'vigentes':  sum(1 for c in carreras if c.estado_rediseno == 'VIGENTE'),
        'proximas':  sum(1 for c in carreras if c.estado_rediseno == 'PROXIMO'),
        'vencidas':  sum(1 for c in carreras if c.estado_rediseno == 'VENCIDO'),
        'sin_datos': sum(1 for c in carreras if c.estado_rediseno == 'SIN_DATOS'),
        'con_rediseno':        len(ids_rediseno & todos_ids),
        'con_diseno':          len(ids_diseno & todos_ids),
        'con_ajuste':          len(ids_ajuste & todos_ids),
        'con_complementacion': len(ids_compl & todos_ids),
        'sin_proceso':         len(todos_ids - ids_con_proceso),
        'total_carreras_int':  len(todos_ids),
        # porcentajes precalculados para evitar widthratio en xhtml2pdf
        'pct_rediseno':        round(len(ids_rediseno & todos_ids) / total_int * 100),
        'pct_diseno':          round(len(ids_diseno & todos_ids) / total_int * 100),
        'pct_ajuste':          round(len(ids_ajuste & todos_ids) / total_int * 100),
        'pct_complementacion': round(len(ids_compl & todos_ids) / total_int * 100),
        'pct_sin_proceso':     round(len(todos_ids - ids_con_proceso) / total_int * 100),
    }

    html_string = render_to_string('reportes/estadisticas_pdf.html', {
        'stats':                    stats,
        'sedes_por_depto':          sedes_por_depto,
        'carreras_por_universidad': carreras_por_universidad,
        'fecha':                    timezone.now(),
    })

    buffer = BytesIO()
    pisa_status = pisa.CreatePDF(html_string, dest=buffer, encoding='utf-8')

    if pisa_status.err:
        return HttpResponse('Error al generar el PDF', status=500)

    buffer.seek(0)
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="estadisticas_sigcu.pdf"'
    return response