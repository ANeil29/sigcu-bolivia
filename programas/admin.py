from django.contrib import admin
from .models import Programa


@admin.register(Programa)
class ProgramaAdmin(admin.ModelAdmin):
    list_display  = ['nombre', 'sede', 'facultad', 'universidad',
                     'estado', 'grado_previsto', 'fecha_prevista_aprobacion', 'activo']
    list_filter   = ['estado', 'grado_previsto', 'activo',
                     'sede__departamento', 'sede__facultad__universidad']
    search_fields = ['nombre', 'sede__facultad__universidad__sigla']
    readonly_fields = ['dias_desde_inicio', 'proximo_a_vencer', 'universidad', 'facultad', 'departamento']