from django.contrib import admin
from django.urls import path, include
from equipos.views import (
    dashboard_view, 
    inventario_view,
    evaluacion_desempeno_view,     # <-- NUEVO
    eliminar_desempeno_view, 
    editar_equipo, 
    eliminar_equipo,
    descargar_pdf_equipo,  # <-- NUEVA VISTA PDF
    evaluacion_view, 
    evaluacion_marketing_view,
    dashboard_marketing_view,
    carga_laboral_view,
    eliminar_carga_view,
    admin_dashboard_view,
    admin_empresa_detalle_view,
    exportar_reporte_csv,
    dashboard_equipo_view,
    evaluacion_view,
    editar_desempeno_view,
    dashboard_persona_desempeno_view,
    dashboard_rrhh_view,
    descargar_pdf_rrhh,
    descargar_pdf_desempeno,
    exportar_reporte_pdf,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('cuentas/', include('django.contrib.auth.urls')),
    path('', dashboard_view, name='dashboard'),
    path('inventario/', inventario_view, name='inventario'),
    path('editar/<int:id>/', editar_equipo, name='editar_equipo'),
    path('eliminar/<int:id>/', eliminar_equipo, name='eliminar_equipo'),
    path('equipo-pdf/<int:id>/', descargar_pdf_equipo, name='descargar_pdf_equipo'),  # <-- NUEVA RUTA
    path('evaluacion-desempeno/', evaluacion_desempeno_view, name='evaluacion_desempeno'),          # <-- NUEVA RUTA
    path('eliminar-desempeno/<int:id>/', eliminar_desempeno_view, name='eliminar_desempeno'),    # <-- NUEVA RUTA
    path('evaluacion/', evaluacion_view, name='evaluacion'),
    path('dashboard-marketing/', dashboard_marketing_view, name='dashboard_marketing'),
    path('evaluacion-marketing/', evaluacion_marketing_view, name='evaluacion_marketing'),
    path('carga-laboral/', carga_laboral_view, name='carga_laboral'),
    path('eliminar-carga/<int:id>/', eliminar_carga_view, name='eliminar_carga'),
    path('panel-admin/', admin_dashboard_view, name='admin_dashboard'),
    path('panel-admin/empresa/<int:user_id>/', admin_empresa_detalle_view, name='admin_empresa_detalle'),
    path('panel-admin/empresa/<int:user_id>/csv/', exportar_reporte_csv, name='exportar_reporte_csv'),
    path('panel-admin/empresa/<int:user_id>/pdf/', exportar_reporte_pdf, name='exportar_reporte_pdf'),
    path('equipo-dashboard/<int:id>/', dashboard_equipo_view, name='dashboard_equipo'),
    path('carga-laboral/', carga_laboral_view, name='carga_laboral'),
    path('eliminar-carga/<int:id>/', eliminar_carga_view, name='eliminar_carga'),
    path('evaluacion-desempeno/', evaluacion_desempeno_view, name='evaluacion_desempeno'),
    path('editar-desempeno/<int:id>/', editar_desempeno_view, name='editar_desempeno'),
    path('eliminar-desempeno/<int:id>/', eliminar_desempeno_view, name='eliminar_desempeno'),
    path('desempeno-persona/<int:id>/', dashboard_persona_desempeno_view, name='dashboard_persona_desempeno'),
    path('dashboard-rrhh/', dashboard_rrhh_view, name='dashboard_rrhh'),
    path('desempeno-persona/<int:id>/', dashboard_persona_desempeno_view, name='dashboard_persona_desempeno'),
    path('desempeno-pdf/<int:id>/', descargar_pdf_desempeno, name='descargar_pdf_desempeno'),
    path('dashboard-rrhh/', dashboard_rrhh_view, name='dashboard_rrhh'),
    path('rrhh-pdf/', descargar_pdf_rrhh, name='descargar_pdf_rrhh'),
    
]