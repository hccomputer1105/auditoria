from django.shortcuts import render

def dashboard_view(request):
    # Más adelante aquí enviaremos los datos de las computadoras a la vista
    return render(request, 'equipos/dashboard.html')