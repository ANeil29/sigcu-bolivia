from django.urls import path
from .views import vista_estadisticas, resumen_estadisticas, exportar_carreras_excel, exportar_estadisticas_pdf

urlpatterns = [
    path('estadisticas/',        vista_estadisticas,       name='vista-estadisticas'),
    path('estadisticas/json/',   resumen_estadisticas,     name='reporte-estadisticas'),
    path('estadisticas/pdf/',    exportar_estadisticas_pdf, name='reporte-estadisticas-pdf'),
    path('carreras/excel/',      exportar_carreras_excel,  name='reporte-carreras-excel'),
]