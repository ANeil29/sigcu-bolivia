from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from rest_framework import viewsets, permissions
from django.contrib.auth import get_user_model

from .forms import FormularioRegistro, FormularioAsignarRol, LoginForm
from .serializers import UsuarioSerializer, RegistroSerializer
from .decorators import rol_requerido

from .models import RegistroActividad
from .middleware import get_ip

Usuario = get_user_model()



def vista_login(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    form = LoginForm(request, data=request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            user = form.get_user()
            if not user.activo_sistema:
                messages.warning(request,
                    'Tu cuenta está pendiente de aprobación. '
                    'El administrador te notificará cuando esté lista.')
                return redirect('login')
            login(request, user)
            RegistroActividad.objects.create(
    usuario=user,
    accion='LOGIN',
    modulo='Autenticación',
    descripcion=f'Inicio de sesión desde {get_ip(request)}',
    ip=get_ip(request),
)
            return redirect('dashboard')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos.')
    return render(request, 'accounts/login.html', {'form': form})


def vista_registro(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    form = FormularioRegistro(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request,
                '✅ Solicitud enviada correctamente. '
                'El administrador revisará tu solicitud y te habilitará el acceso.')
            return redirect('login')
        else:
            messages.error(request, 'Por favor corrige los errores del formulario.')
    return render(request, 'accounts/registro.html', {'form': form})


def vista_logout(request):
    if request.user.is_authenticated:
        RegistroActividad.objects.create(
            usuario=request.user,
            accion='LOGOUT',
            modulo='Autenticación',
            descripcion='Cierre de sesión',
            ip=get_ip(request),
        )
    logout(request)
    return redirect('login')



@login_required
@rol_requerido('SUPERADMIN')
def panel_admin_usuarios(request):
    """Lista todos los usuarios: pendientes primero, luego el resto."""
    pendientes = Usuario.objects.filter(rol='PENDIENTE').order_by('date_joined')
    activos    = Usuario.objects.exclude(rol='PENDIENTE').order_by('rol', 'last_name')
    return render(request, 'accounts/panel_usuarios.html', {
        'pendientes': pendientes,
        'activos':    activos,
    })


@login_required
@rol_requerido('SUPERADMIN')
def aprobar_usuario(request, pk):
    """Aprueba un usuario y le asigna rol."""
    usuario = get_object_or_404(Usuario, pk=pk)
    form    = FormularioAsignarRol(request.POST or None, instance=usuario)
    if request.method == 'POST':
        if form.is_valid():
            u = form.save(commit=False)
            u.is_active       = True
            u.activo_sistema  = True
            u.aprobado_por    = request.user
            u.fecha_aprobacion = timezone.now()
            u.save()
            messages.success(request,
                f'✅ Usuario {u.get_full_name()} aprobado con rol {u.get_rol_display()}.')
            return redirect('panel-admin-usuarios')
    return render(request, 'accounts/aprobar_usuario.html', {
        'usuario': usuario,
        'form':    form,
    })


@login_required
@rol_requerido('SUPERADMIN')
def rechazar_usuario(request, pk):
    usuario = get_object_or_404(Usuario, pk=pk)
    if request.method == 'POST':
        nombre = usuario.get_full_name()
        usuario.delete()
        messages.warning(request, f'Usuario {nombre} rechazado y eliminado.')
        return redirect('panel-admin-usuarios')
    return render(request, 'accounts/confirmar_rechazo.html', {'usuario': usuario})


@login_required
@rol_requerido('SUPERADMIN')
def editar_rol_usuario(request, pk):
    usuario = get_object_or_404(Usuario, pk=pk)
    form    = FormularioAsignarRol(request.POST or None, instance=usuario)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, f'Rol actualizado para {usuario.get_full_name()}.')
            return redirect('panel-admin-usuarios')
    return render(request, 'accounts/editar_rol.html', {
        'usuario': usuario,
        'form':    form,
    })


@login_required
@rol_requerido('SUPERADMIN')
def desactivar_usuario(request, pk):
    usuario = get_object_or_404(Usuario, pk=pk)
    if request.method == 'POST':
        usuario.is_active      = False
        usuario.activo_sistema = False
        usuario.save()
        messages.warning(request, f'Usuario {usuario.get_full_name()} desactivado.')
        return redirect('panel-admin-usuarios')
    return render(request, 'accounts/confirmar_desactivar.html', {'usuario': usuario})



class UsuarioViewSet(viewsets.ModelViewSet):
    queryset         = Usuario.objects.all()
    serializer_class = UsuarioSerializer
    permission_classes = [permissions.IsAdminUser]

from django.contrib.auth.views import (
    PasswordResetView, PasswordResetDoneView,
    PasswordResetConfirmView, PasswordResetCompleteView
)
from .forms import CambiarContrasenaAdminForm


# Recuperación de contraseña por correo

class RecuperarContrasena(PasswordResetView):
    template_name         = 'accounts/recuperar_contrasena.html'
    email_template_name   = 'accounts/email_recuperar_contrasena.html'
    subject_template_name = 'accounts/email_asunto_recuperar.txt'
    success_url           = '/auth/recuperar/enviado/'

class RecuperarContrasenaEnviado(PasswordResetDoneView):
    template_name = 'accounts/recuperar_enviado.html'

class RecuperarContrasenaConfirmar(PasswordResetConfirmView):
    template_name = 'accounts/recuperar_confirmar.html'
    success_url   = '/auth/recuperar/completado/'

class RecuperarContrasenaCompletado(PasswordResetCompleteView):
    template_name = 'accounts/recuperar_completado.html'


# Restablecer contraseña manual (solo Superadmin)

@login_required
@rol_requerido('SUPERADMIN')
def restablecer_contrasena_admin(request, pk):
    usuario = get_object_or_404(Usuario, pk=pk)
    form    = CambiarContrasenaAdminForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        usuario.set_password(form.cleaned_data['nueva_contrasena'])
        usuario.save()
        messages.success(request,
            f'✅ Contraseña de {usuario.get_full_name()} restablecida correctamente.')
        return redirect('panel-admin-usuarios')
    return render(request, 'accounts/restablecer_contrasena_admin.html', {
        'usuario': usuario,
        'form':    form,
    })

@login_required
@rol_requerido('SUPERADMIN')
def panel_auditoria(request):
    from .models import SesionActiva, RegistroActividad
    from django.utils import timezone

    # Usuarios en línea (activos en los últimos 10 minutos)
    hace_10min  = timezone.now() - timezone.timedelta(minutes=10)
    en_linea    = SesionActiva.objects.select_related('usuario').filter(
                      ultimo_acceso__gte=hace_10min
                  ).order_by('-ultimo_acceso')

    # Filtros de auditoría
    usuario_id  = request.GET.get('usuario', '')
    accion      = request.GET.get('accion', '')
    modulo      = request.GET.get('modulo', '')

    actividades = RegistroActividad.objects.select_related('usuario').all()

    if usuario_id:
        actividades = actividades.filter(usuario_id=usuario_id)
    if accion:
        actividades = actividades.filter(accion=accion)
    if modulo:
        actividades = actividades.filter(modulo__icontains=modulo)

    actividades = actividades[:200]  # últimas 200

    todos_usuarios = Usuario.objects.filter(activo_sistema=True).order_by('last_name')

    return render(request, 'accounts/panel_auditoria.html', {
        'en_linea':       en_linea,
        'actividades':    actividades,
        'todos_usuarios': todos_usuarios,
        'filtro_usuario': usuario_id,
        'filtro_accion':  accion,
        'filtro_modulo':  modulo,
        'acciones':       RegistroActividad.ACCION_CHOICES,
    })