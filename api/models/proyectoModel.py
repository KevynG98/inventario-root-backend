from django.db import models

class Proyectos(models.Model):

    # --- Definición de estados del proyecto ---
    PRESUPUESTADO_LANDING = 0
    PRESUPUESTADO_ADMIN = 1
    RECHAZADO = 2
    ACEPTADO = 3
    EN_PROCESO = 4
    DETENIDO = 5
    FINALIZADO = 6
    CANCELADO = 7

    ESTATUS_CHOICES = [
        (PRESUPUESTADO_LANDING, "Presupuestado desde landingPage"),
        (PRESUPUESTADO_ADMIN, "Presupuestado desde portal administrativo"),
        (RECHAZADO, "Proyecto/Presupuesto rechazado"),
        (ACEPTADO, "Proyecto aceptado"),
        (EN_PROCESO, "Proyecto en proceso"),
        (DETENIDO, "Proyecto detenido"),
        (FINALIZADO, "Proyecto finalizado"),
        (CANCELADO, "Proyecto cancelado"),
    ]

    # --- Campos del proyecto ---
    nombreEmpresa = models.CharField(max_length=200)
    nombreProyecto = models.CharField(max_length=200)
    direccionEmpresa = models.TextField()
    telefonoEmpresa = models.CharField(max_length=20)
    emailEmpresa = models.EmailField()
    totalPresupuestado = models.DecimalField(max_digits=12, decimal_places=2)

    estatusProyecto = models.PositiveSmallIntegerField(
        choices=ESTATUS_CHOICES,
        default=PRESUPUESTADO_LANDING,   # Puedes cambiar el estado inicial aquí
    )
    
    ###proyecto.detalleproyectos_set.all() para acceder a los detalles del proyecto