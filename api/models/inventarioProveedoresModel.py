from django.db import models

class Proveedor(models.Model):
    ESTADO_CHOICES = [
        ('alta', 'Alta'),
        ('baja', 'Baja'),
    ]

    LOCALIDAD_CHOICES = [
        ('local', 'Local'),
        ('extranjero', 'Extranjero'),
    ]

    RETENER_ISR_CHOICES = [
        ('si', 'Sí'),
        ('no', 'No'),
    ]

    nit = models.CharField(max_length=20, blank=True, null=True)
    nombre = models.TextField()
    direccion = models.TextField(blank=True, null=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    correo = models.EmailField(blank=True, null=True)
    pagina_web = models.URLField(blank=True, null=True)
    estado = models.CharField(max_length=10, choices=ESTADO_CHOICES, default='alta')
    observaciones = models.TextField(blank=True, null=True)

    tipo = models.CharField(max_length=20, blank=True, null=True)
    dias_credito = models.IntegerField(null=True, blank=True, default=0)
    local_extranjero = models.CharField(max_length=10, choices=LOCALIDAD_CHOICES, default='local')
    pais = models.CharField(max_length=50, default='Guatemala')
    moneda = models.CharField(max_length=50, default='GTQ - QUETZALES')
    retener_isr = models.CharField(max_length=2, choices=RETENER_ISR_CHOICES, default='no')
    regimen_contable = models.CharField(max_length=100, blank=True, null=True)
    cuenta_contable = models.CharField(max_length=100, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    
    cuentas_bancarias = models.JSONField(default=list, blank=True, null=True)

    def __str__(self):
        return self.nombre