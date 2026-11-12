from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Computadora, Perfil, EvaluacionISO

@login_required(login_url='/cuentas/login/')
def dashboard_view(request):
    equipos = Computadora.objects.filter(usuario_empresa=request.user)
    
    total_equipos = equipos.count()
    con_antivirus = equipos.filter(tiene_antivirus=True).count()
    
    context = {
        'total_equipos': total_equipos,
        'con_antivirus': con_antivirus,
    }
    return render(request, 'equipos/dashboard.html', context)


@login_required(login_url='/cuentas/login/')
def inventario_view(request):
    if request.method == 'POST':
        # Recibir los datos del formulario HTML
        nuevo_equipo = Computadora(
            usuario_empresa=request.user, # Asignamos la empresa actual
            tipo_equipo=request.POST.get('tipo_equipo'),
            estatus=request.POST.get('estatus'),
            tiene_antivirus=request.POST.get('tiene_antivirus') == 'on',
            prog_anydesk=request.POST.get('prog_anydesk') == 'on',
            prog_winrar=request.POST.get('prog_winrar') == 'on',
            prog_pdf=request.POST.get('prog_pdf') == 'on',
            prog_office=request.POST.get('prog_office') == 'on',
            version_office=request.POST.get('version_office', ''),
            licencia_office=request.POST.get('licencia_office') == 'on',
            licencia_windows=request.POST.get('licencia_windows') == 'on',
            version_windows=request.POST.get('version_windows', ''),
            licencia_erp=request.POST.get('licencia_erp') == 'on',
            tipo_erp=request.POST.get('tipo_erp', ''),
            
            # Valores por defecto para campos obligatorios antiguos
            nombre_equipo=str(request.POST.get('tipo_equipo')) + " Registrado",
            sistema_operativo="No definido",
            ultima_actualizacion="2024-01-01",
            ultimo_mantenimiento="2024-01-01"
        )
        nuevo_equipo.save() 
        return redirect('inventario')
        
    # Buscar los equipos del usuario actual ordenados por fecha
    mis_equipos = Computadora.objects.filter(usuario_empresa=request.user).order_by('-fecha_auditoria')
    
    # Enviar los equipos al HTML
    return render(request, 'equipos/inventario.html', {'mis_equipos': mis_equipos})


@login_required(login_url='/cuentas/login/')
def eliminar_equipo(request, id):
    # Buscar el equipo asegurando que pertenezca al usuario actual
    equipo = get_object_or_404(Computadora, id=id, usuario_empresa=request.user)
    equipo.delete()
    return redirect('inventario')


@login_required(login_url='/cuentas/login/')
def editar_equipo(request, id):
    equipo = get_object_or_404(Computadora, id=id, usuario_empresa=request.user)
    
    if request.method == 'POST':
        # Actualizar los datos con lo que venga del formulario
        equipo.tipo_equipo = request.POST.get('tipo_equipo')
        equipo.estatus = request.POST.get('estatus')
        equipo.tiene_antivirus = request.POST.get('tiene_antivirus') == 'on'
        equipo.prog_anydesk = request.POST.get('prog_anydesk') == 'on'
        equipo.prog_winrar = request.POST.get('prog_winrar') == 'on'
        equipo.prog_pdf = request.POST.get('prog_pdf') == 'on'
        equipo.prog_office = request.POST.get('prog_office') == 'on'
        equipo.version_office = request.POST.get('version_office', '')
        equipo.licencia_office = request.POST.get('licencia_office') == 'on'
        equipo.licencia_windows = request.POST.get('licencia_windows') == 'on'
        equipo.version_windows = request.POST.get('version_windows', '')
        equipo.licencia_erp = request.POST.get('licencia_erp') == 'on'
        equipo.tipo_erp = request.POST.get('tipo_erp', '')
        equipo.save()
        return redirect('inventario')
        
    return render(request, 'equipos/editar.html', {'equipo': equipo})


@login_required(login_url='/cuentas/login/')
def evaluacion_view(request):
    if request.method == 'POST':
        # Guardar las respuestas de los switches (checkboxes) incluyendo las nuevas secciones
        nueva_evaluacion = EvaluacionISO(
            usuario_empresa=request.user,
            pol_documentada=request.POST.get('pol_documentada') == 'on',
            pol_activos=request.POST.get('pol_activos') == 'on',
            acc_passwords=request.POST.get('acc_passwords') == 'on',
            acc_mfa=request.POST.get('acc_mfa') == 'on',
            acc_bajas=request.POST.get('acc_bajas') == 'on',
            fis_site=request.POST.get('fis_site') == 'on',
            fis_energia=request.POST.get('fis_energia') == 'on',
            ope_respaldos=request.POST.get('ope_respaldos') == 'on',
            ope_pruebas=request.POST.get('ope_pruebas') == 'on',
            ope_antivirus=request.POST.get('ope_antivirus') == 'on',
            ope_parches=request.POST.get('ope_parches') == 'on',
            con_plan=request.POST.get('con_plan') == 'on',
            
            # --- NUEVOS CAMPOS AGREGADOS ---
            srv_dominio=request.POST.get('srv_dominio') == 'on',
            srv_respaldo=request.POST.get('srv_respaldo') == 'on',
            srv_correo=request.POST.get('srv_correo') == 'on',
            srv_telefonia=request.POST.get('srv_telefonia') == 'on',
            srv_dns=request.POST.get('srv_dns') == 'on',
            srv_antivirus=request.POST.get('srv_antivirus') == 'on',
            srv_admin=request.POST.get('srv_admin') == 'on',
            srv_camaras=request.POST.get('srv_camaras') == 'on',
            srv_otros=request.POST.get('srv_otros') == 'on',
            srv_otros_desc=request.POST.get('srv_otros_desc', ''),
            
            web_pagina=request.POST.get('web_pagina') == 'on',
            web_dominio=request.POST.get('web_dominio') == 'on',
            web_hosting=request.POST.get('web_hosting') == 'on',
            web_servicios=request.POST.get('web_servicios') == 'on',
            
            seg_biometrico=request.POST.get('seg_biometrico') == 'on',
            seg_camaras=request.POST.get('seg_camaras') == 'on',
            seg_acceso=request.POST.get('seg_acceso') == 'on',
            
            elec_ups=request.POST.get('elec_ups') == 'on',
            elec_estabilizador=request.POST.get('elec_estabilizador') == 'on',
        )
        nueva_evaluacion.save()
        return redirect('dashboard')
        
    return render(request, 'equipos/evaluacion.html')