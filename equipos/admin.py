from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Computadora, Perfil

# --- CONFIGURACIÓN DE USUARIOS Y EMPRESAS ---

# 1. Crear un bloque integrado para agregar la Empresa dentro del Usuario
class PerfilInline(admin.StackedInline):
    model = Perfil
    can_delete = False
    verbose_name_plural = 'Datos de la Empresa'

# 2. Modificar el administrador de Usuarios por defecto de Django
class UserAdmin(BaseUserAdmin):
    inlines = (PerfilInline,)
    # Columnas que verás en la lista de usuarios
    list_display = ('username', 'email', 'get_empresa', 'is_staff')

    def get_empresa(self, obj):
        try:
            return obj.perfil.nombre_empresa
        except:
            return "Sin empresa asignada"
    get_empresa.short_description = 'Empresa'

# Re-registrar el modelo de Usuario con las nuevas características
admin.site.unregister(User)
admin.site.register(User, UserAdmin)


# --- CONFIGURACIÓN DEL INVENTARIO (COMPUTADORAS) ---

@admin.register(Computadora)
class ComputadoraAdmin(admin.ModelAdmin):
    # Columnas que verás en la tabla de inventario general
    list_display = ('tipo_equipo', 'nombre_equipo', 'usuario_asignado', 'estatus', 'usuario_empresa', 'get_empresa_equipo', 'fecha_auditoria')
    
    # Filtros laterales para buscar rápidamente
    list_filter = ('tipo_equipo', 'estatus', 'usuario_empresa')
    
    # Barra de búsqueda superior
    search_fields = ('nombre_equipo', 'usuario_asignado')

    # Función para jalar el nombre de la empresa a la que pertenece el equipo
    def get_empresa_equipo(self, obj):
        if obj.usuario_empresa:
            try:
                return obj.usuario_empresa.perfil.nombre_empresa
            except:
                return "Sin empresa"
        return "N/A"
    get_empresa_equipo.short_description = 'Empresa Dueña'
