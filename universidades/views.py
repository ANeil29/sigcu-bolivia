from django.http import JsonResponse
from rest_framework import viewsets, permissions
from django_filters.rest_framework import DjangoFilterBackend

from .models import Universidad, Facultad, Sede
from .serializers import UniversidadSerializer, FacultadSerializer, SedeSerializer

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from accounts.decorators import puede_editar, rol_requerido
from .forms import UniversidadForm, FacultadForm, SedeForm

class UniversidadViewSet(viewsets.ModelViewSet):
    queryset         = Universidad.objects.filter(activa=True)
    serializer_class = UniversidadSerializer
    filter_backends  = [DjangoFilterBackend]
    filterset_fields = ['departamento', 'activa']

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.AllowAny()]
        return [permissions.IsAdminUser()]


class FacultadViewSet(viewsets.ModelViewSet):
    queryset         = Facultad.objects.select_related('universidad').all()
    serializer_class = FacultadSerializer
    filter_backends  = [DjangoFilterBackend]
    filterset_fields = ['universidad']

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.AllowAny()]
        return [permissions.IsAdminUser()]


class SedeViewSet(viewsets.ModelViewSet):
    queryset         = Sede.objects.select_related('facultad__universidad').filter(activa=True)
    serializer_class = SedeSerializer
    filter_backends  = [DjangoFilterBackend]
    filterset_fields = ['facultad', 'tipo', 'departamento', 'activa']

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.AllowAny()]
        return [permissions.IsAdminUser()]


def sedes_geojson(request):
    sedes    = Sede.objects.select_related(
                   'facultad__universidad'
               ).filter(activa=True, latitud__isnull=False, longitud__isnull=False)
    features = []
    for s in sedes:
        features.append({
            'type': 'Feature',
            'geometry': {
                'type':        'Point',
                'coordinates': [s.longitud, s.latitud],  
            },
            'properties': {
                'nombre':      s.nombre,
                'facultad':    s.facultad.nombre,
                'universidad': s.facultad.universidad.sigla,
                'ciudad':      s.ciudad,
                'telefono':    s.telefono,
            },
        })
    return JsonResponse({'type': 'FeatureCollection', 'features': features})

@login_required
def lista_universidades(request):
    universidades = Universidad.objects.prefetch_related(
        'facultades__sedes'
    ).order_by('departamento', 'sigla')
    return render(request, 'universidades/lista.html',
                  {'universidades': universidades})


@login_required
@puede_editar
def crear_universidad(request):
    form = UniversidadForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, '✅ Universidad creada correctamente.')
        return redirect('lista-universidades')
    return render(request, 'universidades/form_universidad.html',
                  {'form': form, 'titulo': 'Nueva Universidad', 'accion': 'Crear'})


@login_required
@puede_editar
def editar_universidad(request, pk):
    universidad = get_object_or_404(Universidad, pk=pk)
    form = UniversidadForm(request.POST or None, instance=universidad)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, '✅ Universidad actualizada.')
        return redirect('lista-universidades')
    return render(request, 'universidades/form_universidad.html',
                  {'form': form, 'titulo': f'Editar — {universidad.sigla}',
                   'accion': 'Guardar cambios', 'objeto': universidad})


@login_required
@rol_requerido('SUPERADMIN', 'ADMIN_DSA')
def eliminar_universidad(request, pk):
    universidad = get_object_or_404(Universidad, pk=pk)
    if request.method == 'POST':
        nombre = str(universidad)
        universidad.delete()
        messages.warning(request, f'Universidad {nombre} eliminada.')
        return redirect('lista-universidades')
    return render(request, 'universidades/confirmar_eliminar.html',
                  {'objeto': universidad, 'tipo': 'Universidad'})



@login_required
def lista_facultades(request):
    facultades = Facultad.objects.select_related('universidad').order_by(
        'universidad__sigla', 'nombre')
    return render(request, 'universidades/lista_facultades.html',
                  {'facultades': facultades})


@login_required
@puede_editar
def crear_facultad(request):
    form = FacultadForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, '✅ Facultad creada correctamente.')
        return redirect('lista-facultades')
    return render(request, 'universidades/form_facultad.html',
                  {'form': form, 'titulo': 'Nueva Facultad', 'accion': 'Crear'})


@login_required
@puede_editar
def editar_facultad(request, pk):
    facultad = get_object_or_404(Facultad, pk=pk)
    form = FacultadForm(request.POST or None, instance=facultad)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, '✅ Facultad actualizada.')
        return redirect('lista-facultades')
    return render(request, 'universidades/form_facultad.html',
                  {'form': form, 'titulo': f'Editar — {facultad.nombre}',
                   'accion': 'Guardar cambios', 'objeto': facultad})


@login_required
@rol_requerido('SUPERADMIN', 'ADMIN_DSA')
def eliminar_facultad(request, pk):
    facultad = get_object_or_404(Facultad, pk=pk)
    if request.method == 'POST':
        nombre = str(facultad)
        facultad.delete()
        messages.warning(request, f'Facultad {nombre} eliminada.')
        return redirect('lista-facultades')
    return render(request, 'universidades/confirmar_eliminar.html',
                  {'objeto': facultad, 'tipo': 'Facultad'})


@login_required
def lista_sedes(request):
    sedes = Sede.objects.select_related(
        'facultad__universidad'
    ).order_by('departamento', 'ciudad')
    return render(request, 'universidades/lista_sedes.html', {'sedes': sedes})


@login_required
@puede_editar
def crear_sede(request):
    form = SedeForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, '✅ Sede creada correctamente.')
        return redirect('lista-sedes')
    return render(request, 'universidades/form_sede.html',
                  {'form': form, 'titulo': 'Nueva Sede', 'accion': 'Crear'})


@login_required
@puede_editar
def editar_sede(request, pk):
    sede = get_object_or_404(Sede, pk=pk)
    form = SedeForm(request.POST or None, instance=sede)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, '✅ Sede actualizada.')
        return redirect('lista-sedes')
    return render(request, 'universidades/form_sede.html',
                  {'form': form, 'titulo': f'Editar — {sede.nombre}',
                   'accion': 'Guardar cambios', 'objeto': sede})


@login_required
@rol_requerido('SUPERADMIN', 'ADMIN_DSA')
def eliminar_sede(request, pk):
    sede = get_object_or_404(Sede, pk=pk)
    if request.method == 'POST':
        nombre = str(sede)
        sede.delete()
        messages.warning(request, f'Sede {nombre} eliminada.')
        return redirect('lista-sedes')
    return render(request, 'universidades/confirmar_eliminar.html',
                  {'objeto': sede, 'tipo': 'Sede'})