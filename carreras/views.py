from rest_framework import viewsets, permissions
from django_filters.rest_framework import DjangoFilterBackend
from .models import Carrera, PlanEstudio
from .serializers import CarreraSerializer, PlanEstudioSerializer
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from accounts.decorators import puede_editar, rol_requerido
from .forms import CarreraForm, PlanEstudioForm

class CarreraViewSet(viewsets.ModelViewSet):
    queryset         = Carrera.objects.select_related(
                           'sede__facultad__universidad'
                       ).prefetch_related('procesos', 'planes_estudio')
    serializer_class = CarreraSerializer
    filter_backends  = [DjangoFilterBackend]
    filterset_fields = ['sede', 'grado', 'tipo', 'en_funcionamiento', 'area']

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.AllowAny()]
        return [permissions.IsAdminUser()]

class PlanEstudioViewSet(viewsets.ModelViewSet):
    queryset         = PlanEstudio.objects.select_related('carrera')
    serializer_class = PlanEstudioSerializer
    filter_backends  = [DjangoFilterBackend]
    filterset_fields = ['carrera', 'activo']

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.AllowAny()]
        return [permissions.IsAdminUser()]
@login_required
def lista_carreras(request):
    from seguimiento.models import ProcesoCurricular
    from django.db.models import Count

    carreras = Carrera.objects.select_related(
        'sede__facultad__universidad'
    ).prefetch_related('procesos').filter(en_funcionamiento=True).order_by(
        'sede__facultad__universidad__sigla', 'nombre'
    )

    ids_con_rediseno       = set(ProcesoCurricular.objects.filter(
        tipo_proceso='REDISENO').values_list('carrera_id', flat=True))
    ids_con_diseno         = set(ProcesoCurricular.objects.filter(
        tipo_proceso='DISENO').values_list('carrera_id', flat=True))
    ids_con_ajuste         = set(ProcesoCurricular.objects.filter(
        tipo_proceso='AJUSTE').values_list('carrera_id', flat=True))
    ids_con_complementacion = set(ProcesoCurricular.objects.filter(
        tipo_proceso='COMPLEMENTACION').values_list('carrera_id', flat=True))

    todos_ids = set(carreras.values_list('id', flat=True))
    ids_con_proceso = ids_con_rediseno | ids_con_diseno | ids_con_ajuste | ids_con_complementacion

    conteo = {
        'rediseno':        len(ids_con_rediseno & todos_ids),
        'diseno':          len(ids_con_diseno & todos_ids),
        'ajuste':          len(ids_con_ajuste & todos_ids),
        'complementacion': len(ids_con_complementacion & todos_ids),
        'sin_proceso':     len(todos_ids - ids_con_proceso),
    }

    return render(request, 'carreras/lista.html', {
        'carreras': carreras,
        'conteo':   conteo,
    })


@login_required
@puede_editar
def crear_carrera(request):
    form = CarreraForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, '✅ Carrera creada correctamente.')
        return redirect('lista-carreras')
    return render(request, 'carreras/form_carrera.html',
                  {'form': form, 'titulo': 'Nueva Carrera', 'accion': 'Crear'})


@login_required
@puede_editar
def editar_carrera(request, pk):
    carrera = get_object_or_404(Carrera, pk=pk)
    form    = CarreraForm(request.POST or None, instance=carrera)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, '✅ Carrera actualizada.')
        return redirect('lista-carreras')
    return render(request, 'carreras/form_carrera.html',
                  {'form': form, 'titulo': f'Editar — {carrera.nombre}',
                   'accion': 'Guardar cambios', 'objeto': carrera})


@login_required
@rol_requerido('SUPERADMIN', 'ADMIN_DSA')
def eliminar_carrera(request, pk):
    carrera = get_object_or_404(Carrera, pk=pk)
    if request.method == 'POST':
        nombre = str(carrera)
        carrera.delete()
        messages.warning(request, f'Carrera {nombre} eliminada.')
        return redirect('lista-carreras')
    return render(request, 'carreras/confirmar_eliminar.html',
                  {'objeto': carrera, 'tipo': 'Carrera'})



@login_required
@puede_editar
def crear_plan(request, carrera_pk):
    carrera = get_object_or_404(Carrera, pk=carrera_pk)
    form    = PlanEstudioForm(request.POST or None,
                               initial={'carrera': carrera})
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, '✅ Plan de estudio agregado.')
        return redirect('editar-carrera', pk=carrera_pk)
    return render(request, 'carreras/form_plan.html',
                  {'form': form, 'carrera': carrera,
                   'titulo': f'Nuevo Plan — {carrera.nombre}'})


@login_required
@puede_editar
def editar_plan(request, pk):
    plan = get_object_or_404(PlanEstudio, pk=pk)
    form = PlanEstudioForm(request.POST or None, instance=plan)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, '✅ Plan de estudio actualizado.')
        return redirect('editar-carrera', pk=plan.carrera.pk)
    return render(request, 'carreras/form_plan.html',
                  {'form': form, 'carrera': plan.carrera,
                   'titulo': f'Editar Plan — {plan.carrera.nombre}'})


@login_required
@rol_requerido('SUPERADMIN', 'ADMIN_DSA')
def eliminar_plan(request, pk):
    plan = get_object_or_404(PlanEstudio, pk=pk)
    carrera_pk = plan.carrera.pk
    if request.method == 'POST':
        plan.delete()
        messages.warning(request, 'Plan de estudio eliminado.')
        return redirect('editar-carrera', pk=carrera_pk)
    return render(request, 'carreras/confirmar_eliminar.html',
                  {'objeto': plan, 'tipo': 'Plan de Estudio'})