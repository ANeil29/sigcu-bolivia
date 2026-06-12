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