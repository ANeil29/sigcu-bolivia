from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from rest_framework import viewsets, permissions
from django_filters.rest_framework import DjangoFilterBackend
from accounts.decorators import puede_editar, rol_requerido
from .models import TipoFase, ProcesoCurricular, FaseProceso
from .serializers import TipoFaseSerializer, ProcesoCurricularSerializer, FaseProcesoSerializer
from .forms import TipoFaseForm, ProcesoCurricularForm, FaseProcesoForm



class TipoFaseViewSet(viewsets.ModelViewSet):
    queryset         = TipoFase.objects.filter(activa=True).order_by('orden')
    serializer_class = TipoFaseSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.AllowAny()]
        return [permissions.IsAdminUser()]


class ProcesoCurricularViewSet(viewsets.ModelViewSet):
    queryset = ProcesoCurricular.objects.select_related(
                   'carrera__sede__facultad__universidad'
               ).prefetch_related('fases__tipo_fase')
    serializer_class = ProcesoCurricularSerializer
    filter_backends  = [DjangoFilterBackend]
    filterset_fields = ['carrera', 'tipo_proceso', 'estado']

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.IsAuthenticated()]
        return [permissions.IsAdminUser()]


class FaseProcesoViewSet(viewsets.ModelViewSet):
    queryset         = FaseProceso.objects.select_related('proceso', 'tipo_fase')
    serializer_class = FaseProcesoSerializer
    filter_backends  = [DjangoFilterBackend]
    filterset_fields = ['proceso', 'tipo_fase', 'estado']

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.IsAuthenticated()]
        return [permissions.IsAdminUser()]



@login_required
def lista_tipos_fase(request):
    tipos = TipoFase.objects.order_by('orden')
    return render(request, 'seguimiento/lista_tipos_fase.html', {'tipos': tipos})


@login_required
@puede_editar
def crear_tipo_fase(request):
    form = TipoFaseForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, '✅ Tipo de fase creado.')
        return redirect('lista-tipos-fase')
    return render(request, 'seguimiento/form_tipo_fase.html',
                  {'form': form, 'titulo': 'Nuevo Tipo de Fase', 'accion': 'Crear'})


@login_required
@puede_editar
def editar_tipo_fase(request, pk):
    tipo = get_object_or_404(TipoFase, pk=pk)
    form = TipoFaseForm(request.POST or None, instance=tipo)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, '✅ Tipo de fase actualizado.')
        return redirect('lista-tipos-fase')
    return render(request, 'seguimiento/form_tipo_fase.html',
                  {'form': form, 'titulo': f'Editar — {tipo.nombre}',
                   'accion': 'Guardar', 'objeto': tipo})


@login_required
@rol_requerido('SUPERADMIN')
def eliminar_tipo_fase(request, pk):
    tipo = get_object_or_404(TipoFase, pk=pk)
    if request.method == 'POST':
        tipo.delete()
        messages.warning(request, 'Tipo de fase eliminado.')
        return redirect('lista-tipos-fase')
    return render(request, 'seguimiento/confirmar_eliminar.html',
                  {'objeto': tipo, 'tipo': 'Tipo de Fase',
                   'cancelar_url': 'lista-tipos-fase'})



@login_required
def lista_procesos(request):
    procesos = ProcesoCurricular.objects.select_related(
        'carrera__sede__facultad__universidad'
    ).prefetch_related('fases').order_by('-anio_inicio')
    return render(request, 'seguimiento/lista_procesos.html', {'procesos': procesos})


@login_required
def detalle_proceso(request, pk):
    proceso = get_object_or_404(
        ProcesoCurricular.objects.select_related(
            'carrera__sede__facultad__universidad'
        ).prefetch_related('fases__tipo_fase'),
        pk=pk
    )
    tipos_fase = TipoFase.objects.filter(activa=True).order_by('orden')
    return render(request, 'seguimiento/detalle_proceso.html', {
        'proceso':    proceso,
        'tipos_fase': tipos_fase,
    })


@login_required
@puede_editar
def crear_proceso(request):
    form = ProcesoCurricularForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        proceso = form.save()
        messages.success(request, '✅ Proceso curricular creado.')
        return redirect('detalle-proceso', pk=proceso.pk)
    return render(request, 'seguimiento/form_proceso.html',
                  {'form': form, 'titulo': 'Nuevo Proceso Curricular', 'accion': 'Crear'})


@login_required
@puede_editar
def editar_proceso(request, pk):
    proceso = get_object_or_404(ProcesoCurricular, pk=pk)
    form    = ProcesoCurricularForm(request.POST or None, instance=proceso)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, '✅ Proceso actualizado.')
        return redirect('detalle-proceso', pk=pk)
    return render(request, 'seguimiento/form_proceso.html',
                  {'form': form, 'titulo': f'Editar Proceso — {proceso}',
                   'accion': 'Guardar', 'objeto': proceso})


@login_required
@rol_requerido('SUPERADMIN', 'ADMIN_DSA')
def eliminar_proceso(request, pk):
    proceso = get_object_or_404(ProcesoCurricular, pk=pk)
    if request.method == 'POST':
        proceso.delete()
        messages.warning(request, 'Proceso eliminado.')
        return redirect('lista-procesos')
    return render(request, 'seguimiento/confirmar_eliminar.html',
                  {'objeto': proceso, 'tipo': 'Proceso Curricular',
                   'cancelar_url': 'lista-procesos'})



@login_required
@puede_editar
def crear_fase(request, proceso_pk):
    proceso = get_object_or_404(ProcesoCurricular, pk=proceso_pk)
    form    = FaseProcesoForm(request.POST or None, initial={'proceso': proceso})
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, '✅ Fase agregada.')
        return redirect('detalle-proceso', pk=proceso_pk)
    return render(request, 'seguimiento/form_fase.html',
                  {'form': form, 'proceso': proceso,
                   'titulo': f'Nueva Fase — {proceso}'})


@login_required
@puede_editar
def editar_fase(request, pk):
    fase    = get_object_or_404(FaseProceso, pk=pk)
    form    = FaseProcesoForm(request.POST or None, instance=fase)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, '✅ Fase actualizada.')
        return redirect('detalle-proceso', pk=fase.proceso.pk)
    return render(request, 'seguimiento/form_fase.html',
                  {'form': form, 'proceso': fase.proceso,
                   'titulo': f'Editar Fase — {fase.tipo_fase.nombre}'})


@login_required
@rol_requerido('SUPERADMIN', 'ADMIN_DSA')
def eliminar_fase(request, pk):
    fase = get_object_or_404(FaseProceso, pk=pk)
    proceso_pk = fase.proceso.pk
    if request.method == 'POST':
        fase.delete()
        messages.warning(request, 'Fase eliminada.')
        return redirect('detalle-proceso', pk=proceso_pk)
    return render(request, 'seguimiento/confirmar_eliminar.html',
                  {'objeto': fase, 'tipo': 'Fase',
                   'cancelar_url': None, 'proceso_pk': proceso_pk})