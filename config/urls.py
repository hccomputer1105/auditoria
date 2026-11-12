from django.contrib import admin
from django.urls import path, include
from equipos.views import (
    dashboard_view, 
    inventario_view, 
    editar_equipo, 
    eliminar_equipo, 
    evaluacion_view, 
    evaluacion_marketing_view,
    dashboard_marketing_view
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('cuentas/', include('django.contrib.auth.urls')),
    path('', dashboard_view, name='dashboard'),
    path('inventario/', inventario_view, name='inventario'),
    path('editar/<int:id>/', editar_equipo, name='editar_equipo'),
    path('eliminar/<int:id>/', eliminar_equipo, name='eliminar_equipo'),
    path('evaluacion/', evaluacion_view, name='evaluacion'),
    # Rutas exclusivas de Marketing y Ventas:
    path('dashboard-marketing/', dashboard_marketing_view, name='dashboard_marketing'),
    path('evaluacion-marketing/', evaluacion_marketing_view, name='evaluacion_marketing'),
]
