from django.urls import path
from .views import (
    vista_estadisticas, resumen_estadisticas,
    buscador_carreras,
    exportar_carreras_excel,
    exportar_busqueda_excel, exportar_busqueda_pdf,
    exportar_estadisticas_pdf,
    pdf_carreras, pdf_programas, pdf_informe_completo,
)

urlpatterns = [
    path('estadisticas/',         vista_estadisticas,       name='vista-estadisticas'),
    path('estadisticas/json/',    resumen_estadisticas,     name='reporte-estadisticas'),
    path('estadisticas/pdf/',     exportar_estadisticas_pdf, name='reporte-estadisticas-pdf'),
    path('carreras/excel/',       exportar_carreras_excel,  name='reporte-carreras-excel'),
    path('buscador/',             buscador_carreras,        name='buscador-carreras'),
    path('buscador/excel/',       exportar_busqueda_excel,  name='busqueda-excel'),
    path('buscador/pdf/',         exportar_busqueda_pdf,    name='busqueda-pdf'),
    path('pdf/carreras/',          pdf_carreras,             name='pdf-carreras'),
    path('pdf/programas/',         pdf_programas,            name='pdf-programas'),
    path('pdf/informe-completo/',  pdf_informe_completo,     name='pdf-informe-completo'),
]