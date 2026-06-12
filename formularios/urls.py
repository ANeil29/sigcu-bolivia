from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    FormularioValoracionViewSet,
    lista_formularios, detalle_formulario,
    crear_formulario, editar_formulario, eliminar_formulario,
    exportar_pdf, cambiar_estado,
)

router = DefaultRouter()
router.register('', FormularioValoracionViewSet, basename='formulario')

urlpatterns = [
    path('web/',                        lista_formularios,   name='lista-formularios'),
    path('web/crear/',                  crear_formulario,    name='crear-formulario'),
    path('web/<int:pk>/',               detalle_formulario,  name='detalle-formulario'),
    path('web/<int:pk>/editar/',        editar_formulario,   name='editar-formulario'),
    path('web/<int:pk>/eliminar/',      eliminar_formulario, name='eliminar-formulario'),
    path('web/<int:pk>/pdf/',           exportar_pdf,        name='exportar-pdf'),
    path('web/<int:pk>/estado/',        cambiar_estado,      name='cambiar-estado'),
    path('', include(router.urls)),
]