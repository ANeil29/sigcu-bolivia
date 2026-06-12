from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UniversidadViewSet, FacultadViewSet, SedeViewSet, sedes_geojson,
    lista_universidades, crear_universidad, editar_universidad, eliminar_universidad,
    lista_facultades, crear_facultad, editar_facultad, eliminar_facultad,
    lista_sedes, crear_sede, editar_sede, eliminar_sede,
)

router = DefaultRouter()
router.register('',           UniversidadViewSet, basename='universidad')
router.register('facultades', FacultadViewSet,    basename='facultad')
router.register('sedes',      SedeViewSet,        basename='sede')

urlpatterns = [

    path('sedes/geojson/', sedes_geojson, name='sedes-geojson'),

    path('web/',                    lista_universidades,  name='lista-universidades'),
    path('web/crear/',              crear_universidad,    name='crear-universidad'),
    path('web/<int:pk>/editar/',    editar_universidad,   name='editar-universidad'),
    path('web/<int:pk>/eliminar/',  eliminar_universidad, name='eliminar-universidad'),

    path('web/facultades/',                   lista_facultades,  name='lista-facultades'),
    path('web/facultades/crear/',             crear_facultad,    name='crear-facultad'),
    path('web/facultades/<int:pk>/editar/',   editar_facultad,   name='editar-facultad'),
    path('web/facultades/<int:pk>/eliminar/', eliminar_facultad, name='eliminar-facultad'),

    path('web/sedes/',                   lista_sedes,  name='lista-sedes'),
    path('web/sedes/crear/',             crear_sede,   name='crear-sede'),
    path('web/sedes/<int:pk>/editar/',   editar_sede,  name='editar-sede'),
    path('web/sedes/<int:pk>/eliminar/', eliminar_sede, name='eliminar-sede'),

    path('', include(router.urls)),
]