from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages


def redireccion_por_rol(user):
    """Envía al usuario a su panel correspondiente al iniciar sesión o al ser denegado."""
    if user.is_staff or user.is_superuser:
        return 'admin_dashboard'
    perfil = getattr(user, 'perfil', None)
    if not perfil:
        return 'dashboard'
    if perfil.rol == 'ADMIN_EMPRESA' or perfil.permiso_ti:
        return 'dashboard'
    if perfil.permiso_marketing:
        return 'dashboard_marketing'
    if perfil.permiso_rrhh:
        return 'dashboard_rrhh'
    return 'dashboard'


def requiere_modulo(modulo):
    """
    Decorador para vistas: verifica si el usuario tiene acceso a 'ti', 'marketing', 'rrhh' o 'admin_empresa'.
    """
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if request.user.is_staff or request.user.is_superuser:
                return view_func(request, *args, **kwargs)

            perfil = getattr(request.user, 'perfil', None)
            if not perfil:
                return view_func(request, *args, **kwargs)

            if perfil.rol == 'ADMIN_EMPRESA':
                return view_func(request, *args, **kwargs)

            acceso = False
            if modulo == 'ti' and perfil.permiso_ti:
                acceso = True
            elif modulo == 'marketing' and perfil.permiso_marketing:
                acceso = True
            elif modulo == 'rrhh' and perfil.permiso_rrhh:
                acceso = True

            if not acceso:
                messages.warning(request, "No tienes permisos asignados para acceder a ese módulo.")
                return redirect(redireccion_por_rol(request.user))

            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator