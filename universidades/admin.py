from django.contrib import admin
from .models import Universidad, Facultad, Sede

@admin.register(Universidad)
class UniversidadAdmin(admin.ModelAdmin):
    list_display  = ['sigla', 'nombre', 'departamento', 'activa']
    list_filter   = ['departamento', 'activa']
    search_fields = ['nombre', 'sigla']

@admin.register(Facultad)
class FacultadAdmin(admin.ModelAdmin):
    list_display  = ['nombre', 'universidad', 'decano']
    list_filter   = ['universidad']
    search_fields = ['nombre']

@admin.register(Sede)
class SedeAdmin(admin.ModelAdmin):
    list_display  = ['nombre', 'facultad', 'ciudad', 'departamento', 'tipo', 'activa', 'latitud', 'longitud']
    list_filter   = ['tipo', 'departamento', 'activa']
    search_fields = ['nombre', 'ciudad']