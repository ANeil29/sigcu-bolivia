# carreras/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CarreraViewSet, PlanEstudioViewSet,
    lista_carreras, crear_carrera, editar_carrera, eliminar_carrera,
    crear_plan, editar_plan, eliminar_plan,
)

router = DefaultRouter()
router.register('',       CarreraViewSet,     basename='carrera')
router.register('planes', PlanEstudioViewSet, basename='plan-estudio')

urlpatterns = [
    path('web/',                        lista_carreras,  name='lista-carreras'),
    path('web/crear/',                  crear_carrera,   name='crear-carrera'),
    path('web/<int:pk>/editar/',        editar_carrera,  name='editar-carrera'),
    path('web/<int:pk>/eliminar/',      eliminar_carrera, name='eliminar-carrera'),
    path('web/<int:carrera_pk>/plan/crear/', crear_plan, name='crear-plan'),
    path('web/plan/<int:pk>/editar/',   editar_plan,     name='editar-plan'),
    path('web/plan/<int:pk>/eliminar/', eliminar_plan,   name='eliminar-plan'),
    path('', include(router.urls)),
]