from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario

@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    list_display = ['username', 'email', 'rol', 'universidad', 'is_active']
    list_filter  = ['rol', 'is_active']
    fieldsets    = UserAdmin.fieldsets + (
        ('Datos SIGCU', {'fields': ('rol', 'universidad')}),
    )