from django.contrib import admin
from django.urls import path, include
from equipos.views import dashboard_view, inventario_view, editar_equipo, eliminar_equipo # Nuevas importaciones
from equipos.views import dashboard_view, inventario_view, editar_equipo, eliminar_equipo, evaluacion_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('cuentas/', include('django.contrib.auth.urls')),
    path('', dashboard_view, name='dashboard'),
    path('inventario/', inventario_view, name='inventario'),
    # Nuevas rutas para editar y eliminar
    path('editar/<int:id>/', editar_equipo, name='editar_equipo'),
    path('eliminar/<int:id>/', eliminar_equipo, name='eliminar_equipo'),
    path('evaluacion/', evaluacion_view, name='evaluacion'),
]
