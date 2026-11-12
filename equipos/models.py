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
    # Dueño del registro (Empresa/Usuario)
    usuario_empresa = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    # Identificación básica
    nombre_equipo = models.CharField("Nombre del Equipo", max_length=100)
    usuario_asignado = models.CharField("Usuario Asignado", max_length=100, default="Sin asignar")
    departamento = models.CharField("Departamento", max_length=100, default="General")

    # TIPO Y ESTATUS (Desplegables)
    TIPO_CHOICES = [
        ('Computadora', 'Computadora'),
        ('Monitor', 'Monitor'),
        ('Teclado', 'Teclado'),
        ('Mouse', 'Mouse'),
    ]
    tipo_equipo = models.CharField("Tipo", max_length=50, choices=TIPO_CHOICES, default='Computadora')

    ESTATUS_CHOICES = [
        ('Bueno', 'Bueno'),
        ('Malo', 'Malo'),
        ('En reparación', 'En reparación'),
    ]
    estatus = models.CharField("Estatus", max_length=50, choices=ESTATUS_CHOICES, default='Bueno')

    # PROGRAMAS (Checklist)
    prog_office = models.BooleanField("Office Instalado", default=False)
    version_office = models.CharField("Versión de Office", max_length=50, blank=True, null=True)
    prog_anydesk = models.BooleanField("AnyDesk Instalado", default=False)
    prog_winrar = models.BooleanField("WinRAR Instalado", default=False)
    prog_pdf = models.BooleanField("Lector PDF Instalado", default=False)

    # 4. NUEVOS CAMPOS: LICENCIAS
    licencia_office = models.BooleanField("Licencia de Office", default=False)
    
    licencia_windows = models.BooleanField("Licencia de Windows", default=False)
    version_windows = models.CharField("Versión de Windows", max_length=50, blank=True, null=True)
    
    licencia_erp = models.BooleanField("Licencia de Sistema Administrativo", default=False)
    ERP_CHOICES = [
        ('SAP', 'SAP'),
        ('Galac', 'Galac'),
        ('Profit', 'Profit Plus'),
    ]
    tipo_erp = models.CharField("Tipo de Sistema Administrativo", max_length=50, choices=ERP_CHOICES, blank=True, null=True)

    # Criterios ISO 27001
    tiene_antivirus = models.BooleanField("¿Tiene antivirus activo? (ISO A.8.7)", default=False)
    sistema_operativo = models.CharField("Sistema Operativo", max_length=50, default="No definido")
    ultima_actualizacion = models.DateField("Fecha de última actualización", auto_now_add=True)
    en_dominio = models.BooleanField("¿Está unido al dominio? (ISO A.5.15)", default=False)
    filtro_navegacion = models.BooleanField("¿Tiene filtro de navegación web? (ISO A.8.9)", default=False)
    ultimo_mantenimiento = models.DateField("Fecha de último mantenimiento físico", auto_now_add=True)
    
    fecha_auditoria = models.DateTimeField(auto_now_add=True)

    # 5. Servidores Locales
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

    # 6. Servicios Web
    web_pagina = models.BooleanField("Página Web", default=False)
    web_dominio = models.BooleanField("Dominio", default=False)
    web_hosting = models.BooleanField("Hosting", default=False)
    web_servicios = models.BooleanField("Servicios Web", default=False)

    # 7. Seguridad Perimetral
    seg_biometrico = models.BooleanField("Control Biométrico", default=False)
    seg_camaras = models.BooleanField("Cámaras de Seguridad", default=False)
    seg_acceso = models.BooleanField("Control de Acceso", default=False)

    # 8. Respaldo Eléctrico
    elec_ups = models.BooleanField("UPS", default=False)
    elec_estabilizador = models.BooleanField("Estabilizador de corriente", default=False)

    def __str__(self):
        return f"{self.tipo_equipo}: {self.nombre_equipo} - {self.estatus}"
    # NUEVO MODELO: Cuestionario de Auditoría ISO 27001
class EvaluacionISO(models.Model):
    usuario_empresa = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha_evaluacion = models.DateTimeField(auto_now_add=True)
    
    # 1. Políticas y Organización
    pol_documentada = models.BooleanField("¿Política de seguridad documentada?", default=False)
    pol_activos = models.BooleanField("¿Inventario actualizado de activos TI?", default=False)
    
    # 2. Control de Accesos
    acc_passwords = models.BooleanField("¿Política estricta de contraseñas?", default=False)
    acc_mfa = models.BooleanField("¿Uso de Autenticación Multifactor (MFA)?", default=False)
    acc_bajas = models.BooleanField("¿Proceso formal para revocar accesos a ex-empleados?", default=False)
    
    # 3. Seguridad Física
    fis_site = models.BooleanField("¿Servidores en área segura y restringida?", default=False)
    fis_energia = models.BooleanField("¿UPS y protección eléctrica para sistemas críticos?", default=False)
    
    # 4. Operaciones y Continuidad
    ope_respaldos = models.BooleanField("¿Backups periódicos de información crítica?", default=False)
    ope_pruebas = models.BooleanField("¿Pruebas regulares de restauración de backups?", default=False)
    ope_antivirus = models.BooleanField("¿Protección centralizada de Antivirus/EDR?", default=False)
    ope_parches = models.BooleanField("¿Gestión activa de parches y actualizaciones?", default=False)
    con_plan = models.BooleanField("¿Plan de Continuidad de Negocio (DRP/BCP)?", default=False)

    def __str__(self):
        return f"Evaluación de {self.usuario_empresa.username} - {self.fecha_evaluacion.strftime('%d/%m/%Y')}"