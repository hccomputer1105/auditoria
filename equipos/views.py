from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Computadora, Perfil, EvaluacionISO

@login_required(login_url='/cuentas/login/')
def dashboard_view(request):
    equipos = Computadora.objects.filter(usuario_empresa=request.user)
    total_equipos = equipos.count()
    
    equipos_buenos = equipos.filter(estatus='Bueno').count()
    equipos_reparacion = equipos.filter(estatus='En reparación').count()
    equipos_malos = equipos.filter(estatus='Malo').count()
    
    ultima_evaluacion = EvaluacionISO.objects.filter(usuario_empresa=request.user).order_by('-fecha_evaluacion').first()
    
    score_seguro = 0
    score_inseguro = 100
    puntaje_obtenido = 0
    puntaje_maximo = 42  # 21 reactivos x 2 puntos cada uno
    
    fortalezas = []
    debilidades = []
    oportunidades = []
    amenazas = []
    
    # --- 1. ANÁLISIS DEL INVENTARIO ---
    if total_equipos > 0:
        sin_antivirus = equipos.filter(tiene_antivirus=False).count()
        sin_lic_win = equipos.filter(licencia_windows=False).count()
        sin_lic_office = equipos.filter(prog_office=True, licencia_office=False).count()

        if sin_antivirus == 0:
            fortalezas.append("100% del parque informático cuenta con protección antivirus activa.")
        else:
            debilidades.append(f"{sin_antivirus} equipo(s) carecen de protección antivirus local.")
            amenazas.append("Alta vulnerabilidad ante infecciones por malware o propagación en red local.")

        if equipos_malos > 0 or equipos_reparacion > 0:
            debilidades.append(f"Existen {equipos_malos} equipo(s) dañados y {equipos_reparacion} en reparación.")
            oportunidades.append("Planificar renovación tecnológica para optimizar tiempos de respuesta operativa.")
        else:
            fortalezas.append("El 100% del hardware inventariado se encuentra en estado operativo óptimo.")

        if sin_lic_win > 0 or sin_lic_office > 0:
            debilidades.append("Brechas en el licenciamiento de software base (Windows / Microsoft Office).")
            amenazas.append("Riesgo legal por auditorías de software y falta de parches oficiales de seguridad.")
    else:
        debilidades.append("No se han registrado activos de hardware en el inventario.")
        oportunidades.append("Iniciar el levantamiento de inventario para tener trazabilidad de los activos TI.")

    # --- 2. ANÁLISIS DE LA EVALUACIÓN MULTINORMA ---
    if ultima_evaluacion:
        criterios = {
            'p1_1': ("Alineación estratégica entre el plan de TI y los objetivos del negocio (ISO 38500).", "Compras de TI aisladas sin justificación de costo/beneficio ni aval directivo."),
            'p1_2': ("Roles y responsabilidades del área informática claramente delimitados (Matriz RACI).", "Concentración de funciones sin delimitación o desconocimiento de roles."),
            'p1_3': ("Monitoreo directivo activo sobre el rendimiento y cumplimiento normativo de TI.", "Falta de seguimiento ejecutivo sobre las operaciones tecnológicas."),
            'p2_1': ("Metodología formal de gestión de riesgos aprobada por la gerencia (ISO 27001).", "Inexistencia de matriz de riesgos y análisis periódico de amenazas."),
            'p2_2': ("Declaración de Aplicabilidad (SoA) formal y actualizada.", "Desconocimiento de los controles aplicables o exclusiones sin justificar."),
            'p2_3': ("Control de acceso lógico basado en menor privilegio y autenticación MFA.", "Cuentas compartidas o privilegios excesivos sin control ni revocación."),
            'p2_4': ("Programas periódicos de concienciación en seguridad para el personal.", "Brechas humanas por falta de capacitación ante ingeniería social/phishing."),
            'p3_1': ("Perímetro blindado con monitoreo automatizado de eventos y logs (ISO 27032).", "Falta de análisis de logs de seguridad y filtros contra intrusiones."),
            'p3_2': ("Gestión programada de vulnerabilidades y aplicación de parches.", "Sistemas operativos o aplicaciones obsoletas expuestas a fallos conocidos."),
            'p3_3': ("Procedimiento documentado para detección y contención de incidentes.", "Falta de trazabilidad y ausencia de análisis ante incidentes cibernéticos."),
            'p4_1': ("Catálogo de Servicios y Acuerdos de Nivel de Servicio (SLA) definidos (ISO 20000-1).", "Solicitudes gestionadas sin compromisos de tiempo ni formalización."),
            'p4_2': ("Mesa de ayuda estructurada con clasificación por urgencia e impacto.", "Peticiones de soporte recibidas por canales informales sin seguimiento."),
            'p4_3': ("Gestión de Problemas enfocada en eliminar causas raíz recurrentes.", "Tratamiento meramente reactivo; los incidentes críticos se repiten."),
            'p4_4': ("Control formal de cambios (RFC/CAB) con planes de reversión.", "Modificaciones directas en producción sin pruebas ni autorización previa."),
            'p5_1': ("Análisis de Impacto en el Negocio (BIA) con tiempos RTO/RPO definidos (ISO 22301).", "Desconocimiento del impacto operativo/financiero ante caída de sistemas."),
            'p5_2': ("Respaldos periódicos con pruebas técnicas comprobadas de restauración.", "Backups ejecutados sin verificar si los datos son realmente recuperables."),
            'p5_3': ("Planes de Continuidad (BCP) y Recuperación ante Desastres (DRP) vigentes.", "Ausencia de protocolos para operar ante caída de servidores o ransomware."),
            'p5_4': ("Validación periódica de continuidad mediante simulacros realistas.", "Planes de contingencia teóricos nunca ejecutados ni puestos a prueba."),
            'p6_1': ("Ciclo de vida de desarrollo estructurado con pruebas y control de versiones.", "Pases directos de software a producción sin validación de calidad."),
            'p6_2': ("Proveedores externos y servicios nube monitoreados bajo cláusulas SLA/NDA.", "Dependencia de terceros sin acuerdos de confidencialidad ni control."),
            'p6_3': ("Ciclo de mejora continua activo mediante auditorías internas y cierre de hallazgos.", "Ausencia de auditorías internas o hallazgos desatendidos en el tiempo."),
        }

        for campo, (texto_fortaleza, texto_debilidad) in criterios.items():
            valor = getattr(ultima_evaluacion, campo, 0)
            puntaje_obtenido += valor
            if valor == 2:
                fortalezas.append(texto_fortaleza)
            elif valor == 1:
                oportunidades.append(f"Formalizar y documentar: {texto_fortaleza}")
            else:
                debilidades.append(texto_debilidad)

        # Amenazas críticas derivadas
        if ultima_evaluacion.p5_2 == 0 or ultima_evaluacion.p5_3 == 0:
            amenazas.append("Riesgo crítico de pérdida irreversible de datos y paralización operativa ante Ransomware o desastres.")
        if ultima_evaluacion.p2_3 == 0 or ultima_evaluacion.p3_1 == 0:
            amenazas.append("Alta exposición a ciberataques externos, robo de credenciales y accesos no autorizados.")
        if not ultima_evaluacion.elec_ups:
            debilidades.append("Infraestructura sin respaldo eléctrico ininterrumpido (UPS).")
            amenazas.append("Daño físico en servidores y corrupción de bases de datos por fallos eléctricos.")

        score_seguro = round((puntaje_obtenido / puntaje_maximo) * 100)
        score_inseguro = 100 - score_seguro
    else:
        debilidades.append("Cuestionario de auditoría multinorma pendiente por ejecutar.")
        oportunidades.append("Realizar el diagnóstico inicial en la pestaña 'Evaluación' para establecer la línea base.")

    context = {
        'total_equipos': total_equipos,
        'equipos_buenos': equipos_buenos,
        'equipos_reparacion': equipos_reparacion,
        'equipos_malos': equipos_malos,
        'score_seguro': score_seguro,
        'score_inseguro': score_inseguro,
        'puntaje_obtenido': puntaje_obtenido,
        'puntaje_maximo': puntaje_maximo,
        'tiene_evaluacion': ultima_evaluacion is not None,
        'fortalezas': fortalezas,
        'debilidades': debilidades,
        'oportunidades': oportunidades,
        'amenazas': amenazas,
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
    evaluacion = EvaluacionISO.objects.filter(usuario_empresa=request.user).order_by('-fecha_evaluacion').first()

    if request.method == 'POST':
        if not evaluacion:
            evaluacion = EvaluacionISO(usuario_empresa=request.user)
            
        # Guardar los 21 reactivos numéricos (0, 1 o 2)
        campos_numericos = [
            'p1_1', 'p1_2', 'p1_3',
            'p2_1', 'p2_2', 'p2_3', 'p2_4',
            'p3_1', 'p3_2', 'p3_3',
            'p4_1', 'p4_2', 'p4_3', 'p4_4',
            'p5_1', 'p5_2', 'p5_3', 'p5_4',
            'p6_1', 'p6_2', 'p6_3'
        ]
        for campo in campos_numericos:
            setattr(evaluacion, campo, int(request.POST.get(campo, 0)))

        # Guardar infraestructura complementaria
        evaluacion.srv_dominio = request.POST.get('srv_dominio') == 'on'
        evaluacion.srv_respaldo = request.POST.get('srv_respaldo') == 'on'
        evaluacion.srv_correo = request.POST.get('srv_correo') == 'on'
        evaluacion.srv_telefonia = request.POST.get('srv_telefonia') == 'on'
        evaluacion.srv_dns = request.POST.get('srv_dns') == 'on'
        evaluacion.srv_antivirus = request.POST.get('srv_antivirus') == 'on'
        evaluacion.srv_admin = request.POST.get('srv_admin') == 'on'
        evaluacion.srv_camaras = request.POST.get('srv_camaras') == 'on'
        evaluacion.srv_otros = request.POST.get('srv_otros') == 'on'
        evaluacion.srv_otros_desc = request.POST.get('srv_otros_desc', '')
        
        evaluacion.web_pagina = request.POST.get('web_pagina') == 'on'
        evaluacion.web_dominio = request.POST.get('web_dominio') == 'on'
        evaluacion.web_hosting = request.POST.get('web_hosting') == 'on'
        evaluacion.web_servicios = request.POST.get('web_servicios') == 'on'
        
        evaluacion.seg_biometrico = request.POST.get('seg_biometrico') == 'on'
        evaluacion.seg_camaras = request.POST.get('seg_camaras') == 'on'
        evaluacion.seg_acceso = request.POST.get('seg_acceso') == 'on'
        
        evaluacion.elec_ups = request.POST.get('elec_ups') == 'on'
        evaluacion.elec_estabilizador = request.POST.get('elec_estabilizador') == 'on'
        
        evaluacion.save()
        return redirect('dashboard')
        
    return render(request, 'equipos/evaluacion.html', {'eval': evaluacion})