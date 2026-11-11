from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView
)

from .views import (
    UsuarioViewSet,
    vista_login,
    vista_registro,
    vista_logout,
    panel_admin_usuarios,
    aprobar_usuario,
    rechazar_usuario,
    editar_rol_usuario,
    desactivar_usuario,
    reactivar_usuario,
    RecuperarContrasena,
    RecuperarContrasenaEnviado,
    RecuperarContrasenaConfirmar,
    RecuperarContrasenaCompletado,
    restablecer_contrasena_admin,
    panel_auditoria,
)

router = DefaultRouter()
router.register('usuarios', UsuarioViewSet)

urlpatterns = [

    path('login/', vista_login, name='login'),
    path('registro/', vista_registro, name='registro'),
    path('logout/', vista_logout, name='logout'),

    path(
        'recuperar/',
        RecuperarContrasena.as_view(),
        name='recuperar-contrasena'
    ),
    path(
        'recuperar/enviado/',
        RecuperarContrasenaEnviado.as_view(),
        name='recuperar-enviado'
    ),
    path(
        'recuperar/<uidb64>/<token>/',
        RecuperarContrasenaConfirmar.as_view(),
        name='recuperar-confirmar'
    ),
    path(
        'recuperar/completado/',
        RecuperarContrasenaCompletado.as_view(),
        name='recuperar-completado'
    ),

    path(
        'admin-usuarios/',
        panel_admin_usuarios,
        name='panel-admin-usuarios'
    ),
    path(
        'admin-usuarios/<int:pk>/aprobar/',
        aprobar_usuario,
        name='aprobar-usuario'
    ),
    path(
        'admin-usuarios/<int:pk>/rechazar/',
        rechazar_usuario,
        name='rechazar-usuario'
    ),
    path(
        'admin-usuarios/<int:pk>/editar-rol/',
        editar_rol_usuario,
        name='editar-rol-usuario'
    ),
    path(
        'admin-usuarios/<int:pk>/desactivar/',
        desactivar_usuario,
        name='desactivar-usuario'
    ),
    path('admin-usuarios/<int:pk>/reactivar/',
         reactivar_usuario, 
         name='reactivar-usuario'
    ),
    path(
        'admin-usuarios/<int:pk>/restablecer-contrasena/',
        restablecer_contrasena_admin,
        name='restablecer-contrasena-admin'
    ),

    path(
        'auditoria/',
        panel_auditoria,
        name='panel-auditoria'
    ),

    path('', include(router.urls)),

    path(
        'token/',
        TokenObtainPairView.as_view(),
        name='token_obtain'
    ),
    path(
        'token/refresh/',
        TokenRefreshView.as_view(),
        name='token_refresh'
    ),
]