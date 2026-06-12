from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.template.loader import render_to_string
from django.http import HttpResponse
from rest_framework import viewsets, permissions
from django_filters.rest_framework import DjangoFilterBackend
from accounts.decorators import puede_editar, rol_requerido
from .models import FormularioValoracion
from .serializers import FormularioValoracionSerializer
from .forms import FormularioValoracionForm



class FormularioValoracionViewSet(viewsets.ModelViewSet):
    queryset = FormularioValoracion.objects.select_related(
        'proceso__carrera__sede__facultad__universidad'
    )
    serializer_class = FormularioValoracionSerializer
    filter_backends  = [DjangoFilterBackend]
    filterset_fields = ['proceso', 'estado']

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.IsAuthenticated()]
        return [permissions.IsAdminUser()]



@login_required
def lista_formularios(request):
    estado  = request.GET.get('estado', '')
    buscar  = request.GET.get('buscar', '')

    formularios = FormularioValoracion.objects.select_related(
        'proceso__carrera__sede__facultad__universidad'
    ).order_by('-created_at')

    if estado:
        formularios = formularios.filter(estado=estado)
    if buscar:
        formularios = formularios.filter(codigo__icontains=buscar) | \
                      formularios.filter(proceso__carrera__nombre__icontains=buscar) | \
                      formularios.filter(responsable__icontains=buscar)

    todos       = FormularioValoracion.objects.count()
    borradores  = FormularioValoracion.objects.filter(estado='BORRADOR').count()
    enviados    = FormularioValoracion.objects.filter(estado='ENVIADO').count()
    aprobados   = FormularioValoracion.objects.filter(estado='APROBADO').count()
    observados  = FormularioValoracion.objects.filter(estado='OBSERVADO').count()

    return render(request, 'formularios/lista.html', {
        'formularios': formularios,
        'estado':      estado,
        'buscar':      buscar,
        'contadores': {
            'todos':      todos,
            'borradores': borradores,
            'enviados':   enviados,
            'aprobados':  aprobados,
            'observados': observados,
        },
        'estados': FormularioValoracion.ESTADO_CHOICES,
    })


@login_required
def detalle_formulario(request, pk):
    formulario = get_object_or_404(
        FormularioValoracion.objects.select_related(
            'proceso__carrera__sede__facultad__universidad'
        ),
        pk=pk
    )
    return render(request, 'formularios/detalle.html', {'formulario': formulario})


@login_required
@puede_editar
def crear_formulario(request):
    form = FormularioValoracionForm(request.POST or None, request.FILES or None)
    if request.method == 'POST' and form.is_valid():
        formulario = form.save()
        messages.success(request, f'✅ Formulario {formulario.codigo} creado.')
        return redirect('detalle-formulario', pk=formulario.pk)
    return render(request, 'formularios/form_formulario.html',
                  {'form': form, 'titulo': 'Nuevo Formulario de Valoración',
                   'accion': 'Crear'})


@login_required
@puede_editar
def editar_formulario(request, pk):
    formulario = get_object_or_404(FormularioValoracion, pk=pk)
    form = FormularioValoracionForm(
        request.POST or None,
        request.FILES or None,
        instance=formulario
    )
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, '✅ Formulario actualizado.')
        return redirect('detalle-formulario', pk=pk)
    return render(request, 'formularios/form_formulario.html',
                  {'form': form,
                   'titulo': f'Editar — {formulario.codigo}',
                   'accion': 'Guardar cambios',
                   'objeto': formulario})


@login_required
@rol_requerido('SUPERADMIN', 'ADMIN_DSA')
def eliminar_formulario(request, pk):
    formulario = get_object_or_404(FormularioValoracion, pk=pk)
    if request.method == 'POST':
        codigo = formulario.codigo
        formulario.delete()
        messages.warning(request, f'Formulario {codigo} eliminado.')
        return redirect('lista-formularios')
    return render(request, 'formularios/confirmar_eliminar.html',
                  {'objeto': formulario, 'tipo': 'Formulario de Valoración'})


@login_required
def exportar_pdf(request, pk):
    from xhtml2pdf import pisa
    from io import BytesIO

    formulario = get_object_or_404(
        FormularioValoracion.objects.select_related(
            'proceso__carrera__sede__facultad__universidad'
        ), pk=pk
    )
    html_string = render_to_string(
        'formularios/formulario_pdf.html',
        {'formulario': formulario}
    )
    buffer = BytesIO()
    pisa.CreatePDF(html_string, dest=buffer, encoding='utf-8')
    buffer.seek(0)
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = \
        f'attachment; filename="formulario_{formulario.codigo}.pdf"'
    return response


@login_required
@puede_editar
def cambiar_estado(request, pk):
    """Cambia el estado del formulario directamente desde la lista."""
    formulario = get_object_or_404(FormularioValoracion, pk=pk)
    nuevo_estado = request.POST.get('estado')
    estados_validos = [e[0] for e in FormularioValoracion.ESTADO_CHOICES]
    if nuevo_estado in estados_validos:
        formulario.estado = nuevo_estado
        formulario.save()
        messages.success(request,
            f'Estado actualizado a {formulario.get_estado_display()}.')
    return redirect('detalle-formulario', pk=pk)