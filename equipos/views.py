import csv
import json
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect, get_object_or_404
from .models import Computadora, Perfil, EvaluacionISO, EvaluacionMarketing, EvaluacionCargaLaboral


@login_required(login_url='/cuentas/login/')
def dashboard_view(request):
    if request.user.is_staff:
        return redirect('admin_dashboard')

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
        nuevo_equipo = Computadora(
            usuario_empresa=request.user,
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
            nombre_equipo=str(request.POST.get('tipo_equipo')) + " Registrado",
            sistema_operativo="No definido",
            ultima_actualizacion="2024-01-01",
            ultimo_mantenimiento="2024-01-01"
        )
        nuevo_equipo.save()
        return redirect('inventario')
        
    mis_equipos = Computadora.objects.filter(usuario_empresa=request.user).order_by('-fecha_auditoria')
    return render(request, 'equipos/inventario.html', {'mis_equipos': mis_equipos})


@login_required(login_url='/cuentas/login/')
def eliminar_equipo(request, id):
    equipo = get_object_or_404(Computadora, id=id, usuario_empresa=request.user)
    equipo.delete()
    return redirect('inventario')


@login_required(login_url='/cuentas/login/')
def editar_equipo(request, id):
    equipo = get_object_or_404(Computadora, id=id, usuario_empresa=request.user)
    
    if request.method == 'POST':
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


@login_required(login_url='/cuentas/login/')
def evaluacion_marketing_view(request):
    evaluacion = EvaluacionMarketing.objects.filter(usuario_empresa=request.user).order_by('-fecha_evaluacion').first()

    if request.method == 'POST':
        if not evaluacion:
            evaluacion = EvaluacionMarketing(usuario_empresa=request.user)
            
        codigos = [
            'm1_1', 'm1_2', 'm1_3', 'm1_4', 'm1_5', 'm1_6', 'm1_7', 'm1_8', 'm1_9', 'm1_10', 'm1_11',
            'm2_1', 'm2_2', 'm2_3', 'm2_4', 'm2_5', 'm2_6', 'm2_7', 'm2_8', 'm2_9', 'm2_10', 'm2_11', 'm2_12', 'm2_13', 'm2_14', 'm2_15'
        ]
        
        for cod in codigos:
            setattr(evaluacion, cod, int(request.POST.get(cod, 1)))
            setattr(evaluacion, f"ev_{cod}", request.POST.get(f"ev_{cod}", ""))
            
        evaluacion.save()
        return redirect('dashboard_marketing')
        
    return render(request, 'equipos/evaluacion_marketing.html', {'eval': evaluacion})


@login_required(login_url='/cuentas/login/')
def dashboard_marketing_view(request):
    evaluacion = EvaluacionMarketing.objects.filter(usuario_empresa=request.user).order_by('-fecha_evaluacion').first()
    
    puntaje_c1 = 0
    max_c1 = 55
    puntaje_c2 = 0
    max_c2 = 75
    puntaje_total = 0
    max_total = 130
    
    score_madurez = 0
    score_brecha = 100
    
    fortalezas = []
    debilidades = []
    oportunidades = []
    amenazas = []
    
    plan_smart_30 = []
    plan_smart_60 = []
    plan_smart_90 = []
    
    race_fases = {
        'Reach (Alcance y Atracción)': [],
        'Act (Interacción y Captación)': [],
        'Convert (Conversión y Smarketing)': [],
        'Engage (Fidelización y Postventa)': [],
    }

    if evaluacion:
        campos_c1 = [f'm1_{i}' for i in range(1, 12)]
        campos_c2 = [f'm2_{i}' for i in range(1, 16)]
        
        puntaje_c1 = sum(getattr(evaluacion, c, 1) for c in campos_c1)
        puntaje_c2 = sum(getattr(evaluacion, c, 1) for c in campos_c2)
        puntaje_total = puntaje_c1 + puntaje_c2
        
        score_madurez = round((puntaje_total / max_total) * 100)
        score_brecha = 100 - score_madurez

        criterios_mkt = {
            'm1_1': ("Responsabilidades y metas estratégicas de marketing formalmente documentadas.", "Marketing opera sin metas claras absorbiendo tareas operativas residuales."),
            'm1_2': ("Liderazgo estratégico definido con perfil ejecutivo (CMO/Director) en toma de decisiones.", "Falta de liderazgo especializado en marketing; decisiones reactivas."),
            'm1_3': ("Integración activa del feedback del mercado en el desarrollo de productos/servicios.", "Desconexión entre las necesidades reales del cliente y la oferta comercial."),
            'm1_4': ("Estructura equilibrada entre talento interno y agencias especializadas.", "Sobrecarga operativa por falta de especialistas en áreas clave."),
            'm1_5': ("Hoja de ruta clara de contrataciones clave para escalar el departamento.", "Crecimiento desordenado del equipo comercial y de contenidos."),
            'm1_6': ("Procesos y especialistas dedicados a la creación continua de contenidos y activos.", "Activos digitales desactualizados por falta de capacidad de producción."),
            'm1_7': ("Presupuesto anual asignado formalmente sobre porcentaje de ingresos proyectados.", "Asignación presupuestaria improvisada que impide planificar a mediano plazo."),
            'm1_8': ("Fondo destinado a experimentación y testeo de nuevos canales de adquisición.", "Rigidez estratégica; dependencia de canales tradicionales sin innovación."),
            'm1_9': ("Uso de herramientas colaborativas con flujos de trabajo visibles para el equipo.", "Dispersión operativa en chats y correos sin trazabilidad de proyectos."),
            'm1_10': ("Ecosistema tecnológico integrado (web, formularios, email) sin silos de datos.", "Transferencia manual de prospectos con alto riesgo de pérdida de información."),
            'm1_11': ("Calendario editorial y de campañas planificado con 2 a 4 semanas de anticipación.", "Operación reactiva respondiendo a urgencias de última hora."),
            'm2_1': ("Perfil de Cliente Ideal (ICP / Buyer Persona) consensuado entre marketing y ventas.", "Falta de alineación sobre el segmento objetivo; dispersión de esfuerzos."),
            'm2_2': ("Propuesta Única de Valor (USP) enfocada en beneficios diferenciales claros.", "Comunicación centrada en características técnicas y no en soluciones al cliente."),
            'm2_3': ("Auditoría periódica (benchmark) de precios, tráfico y oferta de competidores.", "Ceguera competitiva ante movimientos de precios y posicionamiento del mercado."),
            'm2_4': ("Diversificación saludable en 2 o 3 canales principales de adquisición de clientes.", "Alta dependencia de un único canal de captación (riesgo de caída abrupta)."),
            'm2_5': ("Sitio web optimizado para conversión con prueba social y CTAs efectivos.", "Tráfico web desaprovechado por falta de llamados a la acción y validación social."),
            'm2_6': ("Equilibrio documentado entre captación orgánica (SEO) y pauta optimizada por CAC.", "Adquisición costosa dependiente exclusivamente de pauta publicitaria."),
            'm2_7': ("Criterios objetivos (Lead Scoring) que diferencian MQL de SQL.", "Entrega de prospectos no calificados que saturan y desgastan al equipo de ventas."),
            'm2_8': ("Acuerdo de Nivel de Servicio (SLA) vigente sobre tiempos de respuesta comercial.", "Demoras en el contacto inicial de leads que enfrían la intención de compra."),
            'm2_9': ("Retroalimentación estructurada de ventas sobre motivos de pérdida de negocios.", "Campañas de marketing sin optimización basada en objeciones reales de cierre."),
            'm2_10': ("CRM centralizado que registra todo el ciclo de vida del cliente hasta el cierre.", "Información comercial fragmentada en hojas de cálculo individuales."),
            'm2_11': ("Medición precisa de rentabilidad mediante métricas ROAS, CAC y LTV.", "Toma de decisiones basada en métricas de vanidad (likes/clics) sin retorno real."),
            'm2_12': ("Flujos automatizados de nutrición (Lead Nurturing) para prospectos fríos.", "Pérdida de oportunidades comerciales que no compran en el primer contacto."),
            'm2_13': ("Estrategia activa para potenciar recompras, renovaciones e ingresos recurrentes.", "Modelo dependiente únicamente de captar clientes nuevos constantemente."),
            'm2_14': ("Monitoreo sistemático de lealtad y satisfacción mediante NPS y Churn Rate.", "Desconocimiento de las causas de abandono o cancelación de clientes."),
            'm2_15': ("Programa estructurado de referidos con incentivos para clientes promotores.", "Desaprovechamiento del canal de recomendación boca a boca."),
        }

        for campo, (txt_f, txt_d) in criterios_mkt.items():
            val = getattr(evaluacion, campo, 1)
            if val == 5:
                fortalezas.append(txt_f)
            elif val == 3:
                oportunidades.append(f"Sistematizar y documentar: {txt_f}")
            else:
                debilidades.append(txt_d)

        if evaluacion.m2_4 == 1:
            amenazas.append("Riesgo crítico de caída de ingresos por dependencia de un único canal de adquisición.")
        if evaluacion.m2_10 == 1 or evaluacion.m2_11 == 1:
            amenazas.append("Pérdida de rentabilidad por inversión publicitaria sin trazabilidad de CAC/LTV en CRM.")
        if evaluacion.m2_3 == 1:
            amenazas.append("Pérdida de cuota de mercado frente a competidores con mejor posicionamiento digital.")
        if evaluacion.m2_14 == 1:
            amenazas.append("Erosión silenciosa de la cartera actual por falta de monitoreo de fuga de clientes (Churn).")

        if evaluacion.m2_1 < 5 or evaluacion.m2_2 < 5:
            plan_smart_30.append("Definir y documentar el ICP y la Propuesta Única de Valor (USP) en un taller conjunto Marketing-Ventas, logrando un 100% de adopción en el pitch comercial en los próximos 30 días.")
        if evaluacion.m2_7 < 5 or evaluacion.m2_8 < 5:
            plan_smart_30.append("Establecer un Acuerdo de Nivel de Servicio (SLA) y reglas de calificación MQL/SQL para reducir el tiempo de primer contacto de ventas a menos de 15 minutos en 30 días.")
        if evaluacion.m2_10 < 5:
            plan_smart_30.append("Centralizar el 100% de los prospectos activos en un CRM único con etapas de embudo definidas durante los primeros 30 días.")
        if not plan_smart_30:
            plan_smart_30.append("Auditar la tasa de conversión actual entre MQL y SQL en el CRM para identificar al menos un 10% de mejora en velocidad de cierre en 30 días.")

        if evaluacion.m2_5 < 5 or evaluacion.m1_11 < 5:
            plan_smart_60.append("Rediseñar las páginas de aterrizaje clave incorporando prueba social y CTAs directos, junto con un calendario editorial anticipado de 4 semanas, para elevar la conversión web en un 15% al día 60.")
        if evaluacion.m2_11 < 5:
            plan_smart_60.append("Implementar un tablero mensual de rentabilidad comercial que calcule CAC, ROAS y LTV por canal de adquisición antes de finalizar el día 60.")
        if evaluacion.m1_9 < 5 or evaluacion.m1_10 < 5:
            plan_smart_60.append("Automatizar la captura de formularios web hacia el CRM y el gestor de proyectos para eliminar el 100% de cargas manuales de leads en 60 días.")
        if not plan_smart_60:
            plan_smart_60.append("Ejecutar al menos 2 pruebas A/B en anuncios y páginas de destino para reducir el Coste de Adquisición de Clientes (CAC) en un 12% al día 60.")

        if evaluacion.m2_12 < 5:
            plan_smart_90.append("Construir e implementar 3 flujos automatizados de Lead Nurturing por email para recuperar al menos un 10% de prospectos fríos en un horizonte de 90 días.")
        if evaluacion.m2_13 < 5 or evaluacion.m2_14 < 5 or evaluacion.m2_15 < 5:
            plan_smart_90.append("Lanzar una encuesta trimestral de NPS y un programa formal de referidos para incrementar los ingresos por recurrencia y recomendación en un 15% al día 90.")
        if evaluacion.m1_4 < 5 or evaluacion.m1_5 < 5:
            plan_smart_90.append("Completar la contratación o asignación de roles especialistas (contenidos/tráfico) según la hoja de ruta organizacional antes de cumplir 90 días.")
        if not plan_smart_90:
            plan_smart_90.append("Escalar el presupuesto en un 20% hacia los 2 canales con mayor LTV/CAC comprobado durante el trimestre (90 días).")

        if evaluacion.m2_4 < 5 or evaluacion.m2_6 < 5:
            race_fases['Reach (Alcance y Atracción)'].append("Diversificar fuentes de tráfico combinando posicionamiento orgánico (SEO) con pauta segmentada por CAC.")
        else:
            race_fases['Reach (Alcance y Atracción)'].append("Canales de adquisición diversificados y estrategia SEO/Paid consolidada.")

        if evaluacion.m2_5 < 5 or evaluacion.m1_11 < 5:
            race_fases['Act (Interacción y Captación)'].append("Optimizar arquitectura persuasiva del sitio web (CTAs y prueba social) y sostener calendario de contenidos.")
        else:
            race_fases['Act (Interacción y Captación)'].append("Ecosistema web con propuesta de valor clara y producción sistemática de contenidos.")

        if evaluacion.m2_7 < 5 or evaluacion.m2_8 < 5 or evaluacion.m2_10 < 5:
            race_fases['Convert (Conversión y Smarketing)'].append("Unificar CRM, aplicar reglas MQL/SQL y exigir cumplimiento de SLA comercial en tiempos de respuesta.")
        else:
            race_fases['Convert (Conversión y Smarketing)'].append("Sinergia Smarketing operativa con trazabilidad completa en CRM y medición de ROAS/CAC.")

        if evaluacion.m2_13 < 5 or evaluacion.m2_14 < 5 or evaluacion.m2_15 < 5:
            race_fases['Engage (Fidelización y Postventa)'].append("Activar secuencias de nutrición, medición periódica de NPS/Churn y programa formal de referidos.")
        else:
            race_fases['Engage (Fidelización y Postventa)'].append("Estrategia de retención activa con monitoreo de lealtad (NPS) y recurrencia.")
    else:
        debilidades.append("Aún no se ha completado la Evaluación de Marketing y Ventas.")
        oportunidades.append("Dirígete a 'Evaluación Marketing' para diagnosticar el área comercial.")

    context = {
        'tiene_evaluacion': evaluacion is not None,
        'puntaje_c1': puntaje_c1,
        'max_c1': max_c1,
        'puntaje_c2': puntaje_c2,
        'max_c2': max_c2,
        'puntaje_total': puntaje_total,
        'max_total': max_total,
        'score_madurez': score_madurez,
        'score_brecha': score_brecha,
        'fortalezas': fortalezas,
        'debilidades': debilidades,
        'oportunidades': oportunidades,
        'amenazas': amenazas,
        'plan_smart_30': plan_smart_30,
        'plan_smart_60': plan_smart_60,
        'plan_smart_90': plan_smart_90,
        'race_fases': race_fases,
    }
    return render(request, 'equipos/dashboard_marketing.html', context)


@login_required(login_url='/cuentas/login/')
def carga_laboral_view(request):
    if request.method == 'POST':
        nueva_carga = EvaluacionCargaLaboral(
            usuario_empresa=request.user,
            nombre_colaborador=request.POST.get('nombre_colaborador'),
            cargo_actual=request.POST.get('cargo_actual'),
            departamento=request.POST.get('departamento'),
            roles_adicionales=request.POST.get('roles_adicionales', ''),
            c1_1=int(request.POST.get('c1_1', 0)),
            c1_2=int(request.POST.get('c1_2', 0)),
            c1_3=int(request.POST.get('c1_3', 0)),
            c2_1=int(request.POST.get('c2_1', 0)),
            c2_2=int(request.POST.get('c2_2', 0)),
            c2_3=int(request.POST.get('c2_3', 0)),
            c3_1=int(request.POST.get('c3_1', 0)),
            c3_2=int(request.POST.get('c3_2', 0)),
            c3_3=int(request.POST.get('c3_3', 0)),
            c4_1=int(request.POST.get('c4_1', 0)),
            c4_2=int(request.POST.get('c4_2', 0)),
            c4_3=int(request.POST.get('c4_3', 0)),
        )
        nueva_carga.save()
        return redirect('carga_laboral')

    evaluaciones = EvaluacionCargaLaboral.objects.filter(usuario_empresa=request.user).order_by('-fecha_evaluacion')
    
    total_evaluados = evaluaciones.count()
    criticos = sum(1 for e in evaluaciones if e.porcentaje_saturacion() > 65)
    moderados = sum(1 for e in evaluaciones if 35 < e.porcentaje_saturacion() <= 65)
    optimos = sum(1 for e in evaluaciones if e.porcentaje_saturacion() <= 35)

    context = {
        'evaluaciones': evaluaciones,
        'total_evaluados': total_evaluados,
        'criticos': criticos,
        'moderados': moderados,
        'optimos': optimos,
    }
    return render(request, 'equipos/carga_laboral.html', context)


@login_required(login_url='/cuentas/login/')
def eliminar_carga_view(request, id):
    registro = get_object_or_404(EvaluacionCargaLaboral, id=id, usuario_empresa=request.user)
    registro.delete()
    return redirect('carga_laboral')


def es_administrador(user):
    return user.is_staff or user.is_superuser


@login_required(login_url='/cuentas/login/')
@user_passes_test(es_administrador, login_url='/')
def admin_dashboard_view(request):
    clientes = User.objects.filter(is_staff=False).order_by('-date_joined')
    
    total_empresas = clientes.count()
    total_equipos_global = Computadora.objects.count()
    total_eval_ti = EvaluacionISO.objects.count()
    total_eval_mkt = EvaluacionMarketing.objects.count()
    total_eval_hr = EvaluacionCargaLaboral.objects.count()
    total_evaluaciones_global = total_eval_ti + total_eval_mkt + total_eval_hr

    empresas_data = []
    nombres_empresas = []
    cantidades_equipos = []

    for cliente in clientes:
        perfil = Perfil.objects.filter(usuario=cliente).first()
        nombre_emp = perfil.nombre_empresa if perfil else f"Empresa ({cliente.username})"
        
        eq_count = Computadora.objects.filter(usuario_empresa=cliente).count()
        tiene_ti = EvaluacionISO.objects.filter(usuario_empresa=cliente).exists()
        tiene_mkt = EvaluacionMarketing.objects.filter(usuario_empresa=cliente).exists()
        hr_count = EvaluacionCargaLaboral.objects.filter(usuario_empresa=cliente).count()

        empresas_data.append({
            'user_id': cliente.id,
            'username': cliente.username,
            'email': cliente.email,
            'nombre_empresa': nombre_emp,
            'fecha_registro': cliente.date_joined,
            'equipos_count': eq_count,
            'tiene_ti': tiene_ti,
            'tiene_mkt': tiene_mkt,
            'hr_count': hr_count,
        })
        
        nombres_empresas.append(nombre_emp)
        cantidades_equipos.append(eq_count)

    context = {
        'total_empresas': total_empresas,
        'total_equipos_global': total_equipos_global,
        'total_evaluaciones_global': total_evaluaciones_global,
        'total_eval_ti': total_eval_ti,
        'total_eval_mkt': total_eval_mkt,
        'total_eval_hr': total_eval_hr,
        'empresas_data': empresas_data,
        'nombres_empresas': json.dumps(nombres_empresas),
        'cantidades_equipos': json.dumps(cantidades_equipos),
    }
    return render(request, 'equipos/admin_dashboard.html', context)


@login_required(login_url='/cuentas/login/')
@user_passes_test(es_administrador, login_url='/')
def admin_empresa_detalle_view(request, user_id):
    cliente = get_object_or_404(User, id=user_id)
    perfil = Perfil.objects.filter(usuario=cliente).first()
    nombre_empresa = perfil.nombre_empresa if perfil else cliente.username

    equipos = Computadora.objects.filter(usuario_empresa=cliente)
    eval_ti = EvaluacionISO.objects.filter(usuario_empresa=cliente).order_by('-fecha_evaluacion').first()
    eval_mkt = EvaluacionMarketing.objects.filter(usuario_empresa=cliente).order_by('-fecha_evaluacion').first()
    evals_hr = EvaluacionCargaLaboral.objects.filter(usuario_empresa=cliente).order_by('-fecha_evaluacion')

    puntaje_ti = 0
    if eval_ti:
        campos_ti = [f'p{d}_{q}' for d, max_q in [(1,3),(2,4),(3,3),(4,4),(5,4),(6,3)] for q in range(1, max_q+1)]
        puntaje_ti = sum(getattr(eval_ti, c, 0) for c in campos_ti)

    puntaje_mkt = 0
    if eval_mkt:
        campos_mkt = [f'm1_{i}' for i in range(1, 12)] + [f'm2_{i}' for i in range(1, 16)]
        puntaje_mkt = sum(getattr(eval_mkt, c, 1) for c in campos_mkt)

    context = {
        'cliente': cliente,
        'nombre_empresa': nombre_empresa,
        'equipos': equipos,
        'eval_ti': eval_ti,
        'puntaje_ti': puntaje_ti,
        'eval_mkt': eval_mkt,
        'puntaje_mkt': puntaje_mkt,
        'evals_hr': evals_hr,
    }
    return render(request, 'equipos/admin_empresa_detalle.html', context)


@login_required(login_url='/cuentas/login/')
@user_passes_test(es_administrador, login_url='/')
def exportar_reporte_csv(request, user_id):
    cliente = get_object_or_404(User, id=user_id)
    perfil = Perfil.objects.filter(usuario=cliente).first()
    nombre_empresa = perfil.nombre_empresa if perfil else cliente.username

    response = HttpResponse(content_type='text/csv; charset=utf-8')
    response['Content-Disposition'] = f'attachment; filename="Reporte_Auditoria_{cliente.username}.csv"'
    response.write('\ufeff')

    writer = csv.writer(response, delimiter=';')
    writer.writerow(['REPORTE CONSOLIDADO DE AUDITORIA EMPRESARIAL'])
    writer.writerow(['Empresa:', nombre_empresa, 'Usuario:', cliente.username, 'Email:', cliente.email])
    writer.writerow([])

    writer.writerow(['--- 1. INVENTARIO DE EQUIPOS TI ---'])
    writer.writerow(['Equipo', 'Tipo', 'Usuario Asignado', 'Departamento', 'Estatus', 'Sistema Operativo', 'Antivirus', 'Lic. Windows', 'Lic. Office'])
    for eq in Computadora.objects.filter(usuario_empresa=cliente):
        writer.writerow([
            eq.nombre_equipo, eq.tipo_equipo, eq.usuario_asignado, eq.departamento,
            eq.estatus, eq.sistema_operativo,
            'Si' if eq.tiene_antivirus else 'No',
            'Si' if eq.licencia_windows else 'No',
            'Si' if eq.licencia_office else 'No'
        ])
    writer.writerow([])

    writer.writerow(['--- 2. AUDITORIA MULTINORMA TI (BASE 42 PTS) ---'])
    eval_ti = EvaluacionISO.objects.filter(usuario_empresa=cliente).first()
    if eval_ti:
        campos_ti = [f'p{d}_{q}' for d, max_q in [(1,3),(2,4),(3,3),(4,4),(5,4),(6,3)] for q in range(1, max_q+1)]
        total_ti = sum(getattr(eval_ti, c, 0) for c in campos_ti)
        writer.writerow(['Puntaje Obtenido:', f'{total_ti} / 42 pts', 'Porcentaje Madurez:', f'{round((total_ti/42)*100)}%'])
    else:
        writer.writerow(['Estado:', 'Pendiente por realizar'])
    writer.writerow([])

    writer.writerow(['--- 3. AUDITORIA MARKETING Y SMARKETING (BASE 130 PTS) ---'])
    eval_mkt = EvaluacionMarketing.objects.filter(usuario_empresa=cliente).first()
    if eval_mkt:
        campos_mkt = [f'm1_{i}' for i in range(1, 12)] + [f'm2_{i}' for i in range(1, 16)]
        total_mkt = sum(getattr(eval_mkt, c, 1) for c in campos_mkt)
        writer.writerow(['Puntaje Obtenido:', f'{total_mkt} / 130 pts', 'Porcentaje Madurez:', f'{round((total_mkt/130)*100)}%'])
    else:
        writer.writerow(['Estado:', 'Pendiente por realizar'])
    writer.writerow([])

    writer.writerow(['--- 4. EVALUACION DE CARGA LABORAL (PUESTOS) ---'])
    writer.writerow(['Colaborador', 'Cargo', 'Departamento', 'Roles Adicionales', 'Saturacion (%)', 'Equivalencia FTE'])
    for hr in EvaluacionCargaLaboral.objects.filter(usuario_empresa=cliente):
        writer.writerow([
            hr.nombre_colaborador, hr.cargo_actual, hr.departamento,
            hr.roles_adicionales or 'Ninguno',
            f'{hr.porcentaje_saturacion()}%', hr.personas_equivalentes()
        ])

    return response