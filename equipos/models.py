from django.db import models

class Computadora(models.Model):
    # 1. Identificación básica
    nombre_equipo = models.CharField("Nombre del Equipo", max_length=100)
    usuario_asignado = models.CharField("Usuario Asignado", max_length=100)
    departamento = models.CharField("Departamento", max_length=100)

    # 2. Criterios de Evaluación ISO 27001
    tiene_antivirus = models.BooleanField("¿Tiene antivirus activo? (ISO A.8.7)", default=False)
    sistema_operativo = models.CharField("Sistema Operativo", max_length=50)
    ultima_actualizacion = models.DateField("Fecha de última actualización (ISO A.8.8)")
    en_dominio = models.BooleanField("¿Está unido al dominio? (ISO A.5.15)", default=False)
    filtro_navegacion = models.BooleanField("¿Tiene filtro de navegación web? (ISO A.8.9)", default=False)
    ultimo_mantenimiento = models.DateField("Fecha de último mantenimiento físico (ISO A.7.13)")
    
    # Fecha automática de cuando se hizo la auditoría
    fecha_auditoria = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nombre_equipo} - {self.departamento}"
