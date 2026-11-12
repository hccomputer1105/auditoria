from django.contrib import admin
from django.urls import path, include
from equipos.views import (
    dashboard_view, 
    inventario_view, 
    editar_equipo, 
    eliminar_equipo, 
    evaluacion_view, 
    evaluacion_marketing_view,
    dashboard_marketing_view,
    carga_laboral_view,
    eliminar_carga_view
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('cuentas/', include('django.contrib.auth.urls')),
    path('', dashboard_view, name='dashboard'),
    path('inventario/', inventario_view, name='inventario'),
    path('editar/<int:id>/', editar_equipo, name='editar_equipo'),
    path('eliminar/<int:id>/', eliminar_equipo, name='eliminar_equipo'),
    path('evaluacion/', evaluacion_view, name='evaluacion'),
    path('dashboard-marketing/', dashboard_marketing_view, name='dashboard_marketing'),
    path('evaluacion-marketing/', evaluacion_marketing_view, name='evaluacion_marketing'),
    # NUEVAS RUTAS DE CARGA LABORAL:
    path('carga-laboral/', carga_laboral_view, name='carga_laboral'),
    path('eliminar-carga/<int:id>/', eliminar_carga_view, name='eliminar_carga'),
]