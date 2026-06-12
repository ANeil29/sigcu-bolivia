from django.contrib import admin
from .models import Carrera, PlanEstudio

@admin.register(Carrera)
class CarreraAdmin(admin.ModelAdmin):
    list_display  = ['nombre', 'sede', 'grado', 'tipo', 'en_funcionamiento', 'estado_rediseno']
    list_filter   = ['grado', 'tipo', 'en_funcionamiento', 'area']
    search_fields = ['nombre', 'programa']
    #readonly_fields = ['estado_rediseno', 'anios_desde_ultimo_rediseno']

@admin.register(PlanEstudio)
class PlanEstudioAdmin(admin.ModelAdmin):
    list_display = ['carrera', 'anio_aprobacion', 'activo']
    list_filter  = ['activo']