from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    TipoFaseViewSet, ProcesoCurricularViewSet, FaseProcesoViewSet,
    lista_tipos_fase, crear_tipo_fase, editar_tipo_fase, eliminar_tipo_fase,
    lista_procesos, detalle_proceso, crear_proceso, editar_proceso, eliminar_proceso,
    crear_fase, editar_fase, eliminar_fase,
)

router = DefaultRouter()
router.register('tipos-fase', TipoFaseViewSet,          basename='tipo-fase')
router.register('procesos',   ProcesoCurricularViewSet, basename='proceso')
router.register('fases',      FaseProcesoViewSet,       basename='fase')

urlpatterns = [

    path('web/tipos-fase/',                   lista_tipos_fase,  name='lista-tipos-fase'),
    path('web/tipos-fase/crear/',             crear_tipo_fase,   name='crear-tipo-fase'),
    path('web/tipos-fase/<int:pk>/editar/',   editar_tipo_fase,  name='editar-tipo-fase'),
    path('web/tipos-fase/<int:pk>/eliminar/', eliminar_tipo_fase, name='eliminar-tipo-fase'),

    path('web/procesos/',                   lista_procesos,  name='lista-procesos'),
    path('web/procesos/crear/',             crear_proceso,   name='crear-proceso'),
    path('web/procesos/<int:pk>/',          detalle_proceso, name='detalle-proceso'),
    path('web/procesos/<int:pk>/editar/',   editar_proceso,  name='editar-proceso'),
    path('web/procesos/<int:pk>/eliminar/', eliminar_proceso, name='eliminar-proceso'),

    path('web/procesos/<int:proceso_pk>/fase/crear/', crear_fase,   name='crear-fase'),
    path('web/fases/<int:pk>/editar/',                editar_fase,  name='editar-fase'),
    path('web/fases/<int:pk>/eliminar/',              eliminar_fase, name='eliminar-fase'),

    path('', include(router.urls)),
]