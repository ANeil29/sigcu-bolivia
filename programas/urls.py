from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ProgramaViewSet,
    lista_programas, crear_programa, editar_programa, eliminar_programa,
)

router = DefaultRouter()
router.register('', ProgramaViewSet, basename='programa')

urlpatterns = [
    path('web/',                   lista_programas,  name='lista-programas'),
    path('web/crear/',             crear_programa,   name='crear-programa'),
    path('web/<int:pk>/editar/',   editar_programa,  name='editar-programa'),
    path('web/<int:pk>/eliminar/', eliminar_programa, name='eliminar-programa'),
    path('', include(router.urls)),
]