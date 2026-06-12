from django.contrib import admin
from .models import FormularioValoracion

@admin.register(FormularioValoracion)
class FormularioAdmin(admin.ModelAdmin):
    list_display  = ['codigo', 'proceso', 'estado', 'fecha_elaboracion', 'responsable']
    list_filter   = ['estado']
    search_fields = ['codigo', 'proceso__carrera__nombre']