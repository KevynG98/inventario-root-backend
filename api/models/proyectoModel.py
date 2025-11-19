from django.db import models

class Proyectos(models.Model):
    nombreEmpresa = models.CharField(max_length=200)
    nombreProyecto = models.CharField(max_length=200)
    direccionEmpresa = models.TextField()
    telefonoEmpresa = models.CharField(max_length=20)
    emailEmpresa = models.EmailField()
    totalPresupuestado= models.DecimalField(max_digits=12, decimal_places=2)    
    ###proyecto.detalleproyectos_set.all() para acceder a los detalles del proyecto