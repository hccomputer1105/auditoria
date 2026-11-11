from django.contrib import admin
from django.urls import path
from equipos.views import dashboard_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', dashboard_view, name='dashboard'), # Esta línea reemplaza al cohete
]
