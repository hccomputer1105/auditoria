from django.shortcuts import render
from .models import Computadora

def dashboard_view(request):
    # Traer todos los equipos de la base de datos
    equipos = Computadora.objects.all()
    
    # Calcular métricas básicas
    total_equipos = equipos.count()
    con_antivirus = equipos.filter(tiene_antivirus=True).count()
    
    # Empaquetar los datos para enviarlos al HTML
    context = {
        'total_equipos': total_equipos,
        'con_antivirus': con_antivirus,
        'equipos': equipos,
    }
    
    return render(request, 'equipos/dashboard.html', context)