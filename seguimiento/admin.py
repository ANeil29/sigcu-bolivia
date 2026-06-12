from django.contrib import admin
from .models import TipoFase, ProcesoCurricular, FaseProceso

@admin.register(TipoFase)
class TipoFaseAdmin(admin.ModelAdmin):
    list_display = ['codigo', 'nombre', 'orden', 'activa']
    ordering     = ['orden']

@admin.register(ProcesoCurricular)
class ProcesoCurricularAdmin(admin.ModelAdmin):
    list_display  = ['carrera', 'tipo_proceso', 'anio_inicio', 'anio_conclusion', 'estado']
    list_filter   = ['tipo_proceso', 'estado']
    search_fields = ['carrera__nombre']

@admin.register(FaseProceso)
class FaseProcesoAdmin(admin.ModelAdmin):
    list_display = ['proceso', 'tipo_fase', 'estado', 'fecha_inicio', 'fecha_conclusion']
    list_filter  = ['estado', 'tipo_fase']