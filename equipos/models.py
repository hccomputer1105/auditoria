from django.db import models
from django.contrib.auth.models import User

# 1. TABLA DE EMPRESAS (PERFIL)
class Perfil(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    nombre_empresa = models.CharField("Nombre de la Empresa", max_length=150)

    def __str__(self):
        return self.nombre_empresa


# 2. TABLA DE INVENTARIO (COMPUTADORAS)
class Computadora(models.Model):
    usuario_empresa = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    nombre_equipo = models.CharField("Nombre del Equipo", max_length=100)
    usuario_asignado = models.CharField("Usuario Asignado", max_length=100, default="Sin asignar")
    departamento = models.CharField("Departamento", max_length=100, default="General")

    TIPO_CHOICES = [('Computadora', 'Computadora'), ('Monitor', 'Monitor'), ('Teclado', 'Teclado'), ('Mouse', 'Mouse')]
    tipo_equipo = models.CharField("Tipo", max_length=50, choices=TIPO_CHOICES, default='Computadora')

    ESTATUS_CHOICES = [('Bueno', 'Bueno'), ('Malo', 'Malo'), ('En reparación', 'En reparación')]
    estatus = models.CharField("Estatus", max_length=50, choices=ESTATUS_CHOICES, default='Bueno')

    prog_office = models.BooleanField("Office Instalado", default=False)
    version_office = models.CharField("Versión de Office", max_length=50, blank=True, null=True)
    prog_anydesk = models.BooleanField("AnyDesk Instalado", default=False)
    prog_winrar = models.BooleanField("WinRAR Instalado", default=False)
    prog_pdf = models.BooleanField("Lector PDF Instalado", default=False)

    tiene_antivirus = models.BooleanField("¿Tiene antivirus activo? (ISO A.8.7)", default=False)
    sistema_operativo = models.CharField("Sistema Operativo", max_length=50, default="No definido")
    ultima_actualizacion = models.DateField("Fecha de última actualización", auto_now_add=True)
    en_dominio = models.BooleanField("¿Está unido al dominio? (ISO A.5.15)", default=False)
    filtro_navegacion = models.BooleanField("¿Tiene filtro de navegación web? (ISO A.8.9)", default=False)
    ultimo_mantenimiento = models.DateField("Fecha de último mantenimiento físico", auto_now_add=True)
    fecha_auditoria = models.DateTimeField(auto_now_add=True)

    # Licencias
    licencia_office = models.BooleanField("Licencia de Office", default=False)
    licencia_windows = models.BooleanField("Licencia de Windows", default=False)
    version_windows = models.CharField("Versión de Windows", max_length=50, blank=True, null=True)
    licencia_erp = models.BooleanField("Licencia de Sistema Administrativo", default=False)
    ERP_CHOICES = [('SAP', 'SAP'), ('Galac', 'Galac'), ('Profit', 'Profit Plus')]
    tipo_erp = models.CharField("Tipo de Sistema Administrativo", max_length=50, choices=ERP_CHOICES, blank=True, null=True)

    def __str__(self):
        return f"{self.tipo_equipo}: {self.nombre_equipo} - {self.estatus}"


# 3. TABLA DE EVALUACIÓN MULTINORMA (38 PUNTOS MÁXIMOS) + INFRAESTRUCTURA
class EvaluacionISO(models.Model):
    NIVEL_CHOICES = [
        (0, 'No cumple (0 pts)'),
        (1, 'Parcial (1 pt)'),
        (2, 'Cumple (2 pts)'),
    ]

    usuario_empresa = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha_evaluacion = models.DateTimeField(auto_now_add=True)
    
    # Dominio 1: Gobierno y Dirección Estratégica (ISO 38500 / 9001)
    p1_1 = models.IntegerField("1.1 Estrategia e Inversiones TI", choices=NIVEL_CHOICES, default=0)
    p1_2 = models.IntegerField("1.2 Roles y Responsabilidades", choices=NIVEL_CHOICES, default=0)
    p1_3 = models.IntegerField("1.3 Supervisión y Cumplimiento", choices=NIVEL_CHOICES, default=0)

    # Dominio 2: Seguridad de la Información y Riesgos (ISO 27001)
    p2_1 = models.IntegerField("2.1 Metodología de Gestión de Riesgos", choices=NIVEL_CHOICES, default=0)
    p2_2 = models.IntegerField("2.2 Declaración de Aplicabilidad (SoA)", choices=NIVEL_CHOICES, default=0)
    p2_3 = models.IntegerField("2.3 Control de Acceso e Identidades", choices=NIVEL_CHOICES, default=0)
    p2_4 = models.IntegerField("2.4 Formación y Concienciación", choices=NIVEL_CHOICES, default=0)

    # Dominio 3: Ciberseguridad y Seguridad en Internet (ISO 27032)
    p3_1 = models.IntegerField("3.1 Protección Perimetral y Monitoreo", choices=NIVEL_CHOICES, default=0)
    p3_2 = models.IntegerField("3.2 Gestión de Vulnerabilidades y Parches", choices=NIVEL_CHOICES, default=0)
    p3_3 = models.IntegerField("3.3 Respuesta a Incidentes Cibernéticos", choices=NIVEL_CHOICES, default=0)

    # Dominio 4: Gestión y Entrega de Servicios TI (ISO 20000-1)
    p4_1 = models.IntegerField("4.1 Catálogo de Servicios y SLAs", choices=NIVEL_CHOICES, default=0)
    p4_2 = models.IntegerField("4.2 Mesa de Ayuda (Helpdesk)", choices=NIVEL_CHOICES, default=0)
    p4_3 = models.IntegerField("4.3 Gestión de Problemas (Causa Raíz)", choices=NIVEL_CHOICES, default=0)
    p4_4 = models.IntegerField("4.4 Control de Cambios (RFC/CAB)", choices=NIVEL_CHOICES, default=0)

    # Dominio 5: Continuidad del Negocio y Resiliencia (ISO 22301)
    p5_1 = models.IntegerField("5.1 Análisis de Impacto (BIA)", choices=NIVEL_CHOICES, default=0)
    p5_2 = models.IntegerField("5.2 Copias de Seguridad y Pruebas", choices=NIVEL_CHOICES, default=0)
    p5_3 = models.IntegerField("5.3 Planes DRP / BCP Documentados", choices=NIVEL_CHOICES, default=0)
    p5_4 = models.IntegerField("5.4 Simulacros de Continuidad", choices=NIVEL_CHOICES, default=0)

    # Dominio 6: Calidad y Desarrollo de Software (ISO 9001 / 29110)
    p6_1 = models.IntegerField("6.1 Ciclo de Vida de Desarrollo", choices=NIVEL_CHOICES, default=0)
    p6_2 = models.IntegerField("6.2 Evaluación de Proveedores y Nube", choices=NIVEL_CHOICES, default=0)
    p6_3 = models.IntegerField("6.3 Auditorías Internas y Mejora Continua", choices=NIVEL_CHOICES, default=0)

    # Infraestructura Física y Lógica (Checks Complementarios)
    srv_dominio = models.BooleanField("Servidor de Dominio", default=False)
    srv_respaldo = models.BooleanField("Servidor de Respaldo", default=False)
    srv_correo = models.BooleanField("Servidor de Correo", default=False)
    srv_telefonia = models.BooleanField("Servidor de Telefonía", default=False)
    srv_dns = models.BooleanField("Servidor DNS", default=False)
    srv_antivirus = models.BooleanField("Servidor de Antivirus", default=False)
    srv_admin = models.BooleanField("Servidor Administrativo", default=False)
    srv_camaras = models.BooleanField("Servidor de Cámaras", default=False)
    srv_otros = models.BooleanField("Otros Servidores", default=False)
    srv_otros_desc = models.CharField("Descripción de otros", max_length=200, blank=True, null=True)

    web_pagina = models.BooleanField("Página Web", default=False)
    web_dominio = models.BooleanField("Dominio", default=False)
    web_hosting = models.BooleanField("Hosting", default=False)
    web_servicios = models.BooleanField("Servicios Web", default=False)

    seg_biometrico = models.BooleanField("Control Biométrico", default=False)
    seg_camaras = models.BooleanField("Cámaras de Seguridad", default=False)
    seg_acceso = models.BooleanField("Control de Acceso", default=False)
    elec_ups = models.BooleanField("UPS", default=False)
    elec_estabilizador = models.BooleanField("Estabilizador de corriente", default=False)

    def __str__(self):
        return f"Auditoría Multinorma - {self.usuario_empresa.username}"
    # 4. TABLA DE EVALUACIÓN DE MARKETING Y VENTAS (SMARKETING)
class EvaluacionMarketing(models.Model):
    ESCALA_CHOICES = [
        (1, '1 - Inexistente / No implementado'),
        (3, '3 - En desarrollo / Parcial'),
        (5, '5 - Consolidado / Documentado'),
    ]

    usuario_empresa = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha_evaluacion = models.DateTimeField(auto_now_add=True)

    # --- CUESTIONARIO 1: ESTRUCTURACIÓN ORGANIZACIONAL ---
    # 1. Delimitación de Funciones y Gobernanza
    m1_1 = models.IntegerField("1.1 Responsabilidades documentadas", choices=ESCALA_CHOICES, default=1)
    ev_m1_1 = models.CharField("Evidencia 1.1", max_length=255, blank=True, null=True)
    m1_2 = models.IntegerField("1.2 Liderazgo estratégico (CMO)", choices=ESCALA_CHOICES, default=1)
    ev_m1_2 = models.CharField("Evidencia 1.2", max_length=255, blank=True, null=True)
    m1_3 = models.IntegerField("1.3 Participación en feedback de producto", choices=ESCALA_CHOICES, default=1)
    ev_m1_3 = models.CharField("Evidencia 1.3", max_length=255, blank=True, null=True)

    # 2. Talento y Estructura Organizativa
    m1_4 = models.IntegerField("2.1 Roles internos y agencias", choices=ESCALA_CHOICES, default=1)
    ev_m1_4 = models.CharField("Evidencia 2.1", max_length=255, blank=True, null=True)
    m1_5 = models.IntegerField("2.2 Plan de contratación clave", choices=ESCALA_CHOICES, default=1)
    ev_m1_5 = models.CharField("Evidencia 2.2", max_length=255, blank=True, null=True)
    m1_6 = models.IntegerField("2.3 Especialistas en contenidos y activos", choices=ESCALA_CHOICES, default=1)
    ev_m1_6 = models.CharField("Evidencia 2.3", max_length=255, blank=True, null=True)

    # 3. Presupuesto y Asignación de Recursos
    m1_7 = models.IntegerField("3.1 Determinación formal del presupuesto", choices=ESCALA_CHOICES, default=1)
    ev_m1_7 = models.CharField("Evidencia 3.1", max_length=255, blank=True, null=True)
    m1_8 = models.IntegerField("3.2 Presupuesto para experimentación", choices=ESCALA_CHOICES, default=1)
    ev_m1_8 = models.CharField("Evidencia 3.2", max_length=255, blank=True, null=True)

    # 4. Pila Tecnológica (Tech Stack) y Procesos
    m1_9 = models.IntegerField("4.1 Herramientas integradas de gestión", choices=ESCALA_CHOICES, default=1)
    ev_m1_9 = models.CharField("Evidencia 4.1", max_length=255, blank=True, null=True)
    m1_10 = models.IntegerField("4.2 Automatización entre plataformas", choices=ESCALA_CHOICES, default=1)
    ev_m1_10 = models.CharField("Evidencia 4.2", max_length=255, blank=True, null=True)
    m1_11 = models.IntegerField("4.3 Calendario editorial anticipado", choices=ESCALA_CHOICES, default=1)
    ev_m1_11 = models.CharField("Evidencia 4.3", max_length=255, blank=True, null=True)

    # --- CUESTIONARIO 2: ESTRATEGIA Y SMARKETING ---
    # 1. Propuesta de Valor, Audiencia y Competencia
    m2_1 = models.IntegerField("1.1 Perfil de Cliente Ideal (ICP)", choices=ESCALA_CHOICES, default=1)
    ev_m2_1 = models.CharField("Evidencia Smarketing 1.1", max_length=255, blank=True, null=True)
    m2_2 = models.IntegerField("1.2 Beneficios diferenciales (USP)", choices=ESCALA_CHOICES, default=1)
    ev_m2_2 = models.CharField("Evidencia Smarketing 1.2", max_length=255, blank=True, null=True)
    m2_3 = models.IntegerField("1.3 Auditoría periódica de competencia", choices=ESCALA_CHOICES, default=1)
    ev_m2_3 = models.CharField("Evidencia Smarketing 1.3", max_length=255, blank=True, null=True)

    # 2. Ecosistema de Adquisición y Conversión
    m2_4 = models.IntegerField("2.1 Diversificación de canales de clientes", choices=ESCALA_CHOICES, default=1)
    ev_m2_4 = models.CharField("Evidencia Smarketing 2.1", max_length=255, blank=True, null=True)
    m2_5 = models.IntegerField("2.2 Conversión web, prueba social y CTAs", choices=ESCALA_CHOICES, default=1)
    ev_m2_5 = models.CharField("Evidencia Smarketing 2.2", max_length=255, blank=True, null=True)
    m2_6 = models.IntegerField("2.3 Estrategia SEO y pauta optimizada por CAC", choices=ESCALA_CHOICES, default=1)
    ev_m2_6 = models.CharField("Evidencia Smarketing 2.3", max_length=255, blank=True, null=True)

    # 3. Alineación Marketing-Ventas (Smarketing y SLA)
    m2_7 = models.IntegerField("3.1 Criterios claros MQL vs SQL", choices=ESCALA_CHOICES, default=1)
    ev_m2_7 = models.CharField("Evidencia Smarketing 3.1", max_length=255, blank=True, null=True)
    m2_8 = models.IntegerField("3.2 SLA de tiempo de contacto de ventas", choices=ESCALA_CHOICES, default=1)
    ev_m2_8 = models.CharField("Evidencia Smarketing 3.2", max_length=255, blank=True, null=True)
    m2_9 = models.IntegerField("3.3 Retroalimentación de ventas sobre pérdidas", choices=ESCALA_CHOICES, default=1)
    ev_m2_9 = models.CharField("Evidencia Smarketing 3.3", max_length=255, blank=True, null=True)

    # 4. Medición, CRM y Madurez de Datos
    m2_10 = models.IntegerField("4.1 CRM centralizado de ciclo completo", choices=ESCALA_CHOICES, default=1)
    ev_m2_10 = models.CharField("Evidencia Smarketing 4.1", max_length=255, blank=True, null=True)
    m2_11 = models.IntegerField("4.2 Medición de ROAS, CAC y LTV", choices=ESCALA_CHOICES, default=1)
    ev_m2_11 = models.CharField("Evidencia Smarketing 4.2", max_length=255, blank=True, null=True)
    m2_12 = models.IntegerField("4.3 Flujos automatizados de nutrición (Email)", choices=ESCALA_CHOICES, default=1)
    ev_m2_12 = models.CharField("Evidencia Smarketing 4.3", max_length=255, blank=True, null=True)

    # 5. Retención, Fidelización y Postventa
    m2_13 = models.IntegerField("5.1 Ingresos por recompras y recurrencia", choices=ESCALA_CHOICES, default=1)
    ev_m2_13 = models.CharField("Evidencia Smarketing 5.1", max_length=255, blank=True, null=True)
    m2_14 = models.IntegerField("5.2 Medición de NPS y Churn Rate", choices=ESCALA_CHOICES, default=1)
    ev_m2_14 = models.CharField("Evidencia Smarketing 5.2", max_length=255, blank=True, null=True)
    m2_15 = models.IntegerField("5.3 Programa estructurado de referidos", choices=ESCALA_CHOICES, default=1)
    ev_m2_15 = models.CharField("Evidencia Smarketing 5.3", max_length=255, blank=True, null=True)

    def __str__(self):
        return f"Auditoría Marketing - {self.usuario_empresa.username}"

    # 5. TABLA DE EVALUACIÓN DE CARGA LABORAL Y DIMENSIONAMIENTO DE PUESTOS
class EvaluacionCargaLaboral(models.Model):
    FRECUENCIA_CHOICES = [
        (0, '0 - Nunca / No aplica'),
        (1, '1 - Rara vez (Ocasional)'),
        (2, '2 - A veces (Semanalmente)'),
        (3, '3 - Frecuentemente (Casi a diario)'),
        (4, '4 - Siempre (Constante / Crítico)'),
    ]

    usuario_empresa = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha_evaluacion = models.DateTimeField(auto_now_add=True)

    # Identificación del Puesto
    nombre_colaborador = models.CharField("Nombre del Colaborador", max_length=120)
    cargo_actual = models.CharField("Cargo Oficial", max_length=120)
    departamento = models.CharField("Departamento", max_length=100)
    roles_adicionales = models.CharField("Otros roles que desempeña en la práctica", max_length=255, blank=True, null=True)

    # Dimensión 1: Multifuncionalidad y Dispersión de Roles (Efecto 3 en 1)
    c1_1 = models.IntegerField("1.1 Desempeña funciones de 2 o más cargos distintos", choices=FRECUENCIA_CHOICES, default=0)
    c1_2 = models.IntegerField("1.2 Asume tareas residuales que nadie más quiere o sabe hacer", choices=FRECUENCIA_CHOICES, default=0)
    c1_3 = models.IntegerField("1.3 Cambia abruptamente de contexto entre tareas operativas y estratégicas", choices=FRECUENCIA_CHOICES, default=0)

    # Dimensión 2: Volumen de Trabajo y Presión Temporal
    c2_1 = models.IntegerField("2.1 La jornada laboral normal (8h) es insuficiente para cumplir metas", choices=FRECUENCIA_CHOICES, default=0)
    c2_2 = models.IntegerField("2.2 Trabaja horas extras, fines de semana o fuera de horario", choices=FRECUENCIA_CHOICES, default=0)
    c2_3 = models.IntegerField("2.3 Acumula tareas pendientes (backlog) que crecen cada semana", choices=FRECUENCIA_CHOICES, default=0)

    # Dimensión 3: Cuellos de Botella y Dependencia Crítica
    c3_1 = models.IntegerField("3.1 Si se ausenta o enferma, los procesos clave se detienen", choices=FRECUENCIA_CHOICES, default=0)
    c3_2 = models.IntegerField("3.2 No cuenta con un respaldo (backup humano) capacitado para cubrirlo", choices=FRECUENCIA_CHOICES, default=0)
    c3_3 = models.IntegerField("3.3 Múltiples departamentos dependen simultáneamente de sus entregas", choices=FRECUENCIA_CHOICES, default=0)

    # Dimensión 4: Desgaste Cognitivo y Riesgo Psicosocial
    c4_1 = models.IntegerField("4.1 Sufre interrupciones constantes (llamadas, chats, urgencias)", choices=FRECUENCIA_CHOICES, default=0)
    c4_2 = models.IntegerField("4.2 Omite pausas activas o tiempo de almuerzo por carga operativa", choices=FRECUENCIA_CHOICES, default=0)
    c4_3 = models.IntegerField("4.3 Reporta agotamiento mental, estrés alto o aumento de errores", choices=FRECUENCIA_CHOICES, default=0)

    def puntaje_total(self):
        return (self.c1_1 + self.c1_2 + self.c1_3 +
                self.c2_1 + self.c2_2 + self.c2_3 +
                self.c3_1 + self.c3_2 + self.c3_3 +
                self.c4_1 + self.c4_2 + self.c4_3)

    def porcentaje_saturacion(self):
        return round((self.puntaje_total() / 48) * 100)

    def personas_equivalentes(self):
        # Estimación de FTE (Full-Time Equivalent) basada en saturación
        pct = self.porcentaje_saturacion()
        if pct <= 35:
            return "1.0 persona (Óptimo)"
        elif pct <= 55:
            return "1.5 personas (Sobrecarga leve)"
        elif pct <= 75:
            return "2.0 personas (Doble carga)"
        else:
            return "2.5 a 3.0+ personas (Crítico)"

    def __str__(self):
        return f"{self.cargo_actual} ({self.nombre_colaborador}) - {self.porcentaje_saturacion()}%"