from django.shortcuts import redirect
from django.contrib import messages
from functools import wraps


def rol_requerido(*roles):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('login')
            if request.user.rol not in roles:
                messages.error(request, 'No tienes permisos para acceder a esta sección.')
                return redirect('dashboard')
            if not request.user.activo_sistema:
                messages.error(request, 'Tu cuenta aún no ha sido aprobada.')
                return redirect('login')
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator


def puede_editar(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        if not request.user.activo_sistema:
            return redirect('login')
        if not request.user.puede_editar:
            messages.error(request, 'No tienes permisos para realizar esta acción.')
            return redirect('dashboard')
        return view_func(request, *args, **kwargs)
    return wrapper