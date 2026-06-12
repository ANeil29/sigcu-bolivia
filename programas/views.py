from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from rest_framework import viewsets, permissions
from django_filters.rest_framework import DjangoFilterBackend
from accounts.decorators import puede_editar, rol_requerido
from .models import Programa
from .serializers import ProgramaSerializer
from .forms import ProgramaForm


class ProgramaViewSet(viewsets.ModelViewSet):
    queryset         = Programa.objects.select_related('sede__facultad__universidad')
    serializer_class = ProgramaSerializer
    filter_backends  = [DjangoFilterBackend]
    filterset_fields = ['sede', 'estado', 'area', 'activo']

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.IsAuthenticated()]
        return [permissions.IsAdminUser()]


@login_required
def lista_programas(request):
    from carreras.models import Carrera

    programas = Programa.objects.select_related(
        'sede__facultad__universidad'
    ).filter(activo=True).order_by(
        'sede__facultad__universidad__sigla', 'nombre'
    )

    todos = list(programas)

    ya_carrera = sum(
        1 for p in todos
        if p.estado == 'IMPLEMENTACION' and (
            'RAN' in (p.observaciones or '') or
            'UAGRM' in (p.observaciones or '') or
            'UAJMS' in (p.observaciones or '')
        )
    )

    conteo = {
        'formulacion':    sum(1 for p in todos if p.estado == 'FORMULACION'),
        'aprobacion':     sum(1 for p in todos if p.estado == 'APROBACION'),
        'implementacion': sum(1 for p in todos if p.estado == 'IMPLEMENTACION'),
        'suspendido':     sum(1 for p in todos if p.estado == 'SUSPENDIDO'),
        'ya_carrera':     ya_carrera,
    }

    return render(request, 'programas/lista.html', {
        'programas':      programas,
        'programas_todos': todos,
        'conteo':         conteo,
    })


@login_required
@puede_editar
def crear_programa(request):
    form = ProgramaForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, '✅ Programa creado correctamente.')
        return redirect('lista-programas')
    return render(request, 'programas/form_programa.html',
                  {'form': form, 'titulo': 'Nuevo Programa', 'accion': 'Crear'})


@login_required
@puede_editar
def editar_programa(request, pk):
    programa = get_object_or_404(Programa, pk=pk)
    form     = ProgramaForm(request.POST or None, instance=programa)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, '✅ Programa actualizado.')
        return redirect('lista-programas')
    return render(request, 'programas/form_programa.html',
                  {'form': form, 'titulo': f'Editar — {programa.nombre}',
                   'accion': 'Guardar cambios', 'objeto': programa})


@login_required
@rol_requerido('SUPERADMIN', 'ADMIN_DSA')
def eliminar_programa(request, pk):
    programa = get_object_or_404(Programa, pk=pk)
    if request.method == 'POST':
        nombre = str(programa)
        programa.delete()
        messages.warning(request, f'Programa {nombre} eliminado.')
        return redirect('lista-programas')
    return render(request, 'programas/confirmar_eliminar.html',
                  {'objeto': programa, 'tipo': 'Programa'})