from django.db import models

class Paciente(models.Model):
    nombre = models.CharField(max_length=100)
    fecha_nacimiento = models.DateField(null=True, blank=True)
    edad = models.IntegerField(null=True, blank=True)
    direccion = models.TextField(blank=True)
    telefono1 = models.CharField(max_length=20, blank=True)
    telefono2 = models.CharField(max_length=20, blank=True)
    correo = models.EmailField(blank=True)
    observacion = models.TextField(blank=True)
    religion = models.CharField(max_length=50, blank=True)
    tipo_identificacion = models.CharField(max_length=50, blank=True)
    numero_identificacion = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return self.nombre

class Acompanante(models.Model):
    nombre = models.CharField(max_length=100)
    telefono = models.CharField(max_length=20)

    def __str__(self):
        return self.nombre

class Responsable(models.Model):
    primer_nombre = models.CharField(max_length=50)
    segundo_nombre = models.CharField(max_length=50, blank=True)
    primer_apellido = models.CharField(max_length=50)
    segundo_apellido = models.CharField(max_length=50, blank=True)
    tipo_identificacion = models.CharField(max_length=50)
    numero_identificacion = models.CharField(max_length=50)
    fecha_nacimiento = models.DateField(null=True, blank=True)
    edad = models.IntegerField(null=True, blank=True)
    genero = models.CharField(max_length=20)
    relacion_paciente = models.CharField(max_length=50)
    ocupacion = models.CharField(max_length=100, blank=True)
    domicilio = models.TextField(blank=True)
    empresa = models.CharField(max_length=100, blank=True)
    direccion = models.TextField(blank=True)
    telefono1 = models.CharField(max_length=20, blank=True)
    telefono2 = models.CharField(max_length=20, blank=True)
    contacto = models.CharField(max_length=100, blank=True)
    email = models.EmailField(blank=True)

    def __str__(self):
        return f"{self.primer_nombre} {self.primer_apellido}"

class Esposo(models.Model):
    nombre = models.CharField(max_length=100)
    genero = models.CharField(max_length=20)
    tipo_identificacion = models.CharField(max_length=50)
    numero_identificacion = models.CharField(max_length=50)
    fecha_nacimiento = models.DateField(null=True, blank=True)
    edad = models.IntegerField(null=True, blank=True)
    telefono1 = models.CharField(max_length=20, blank=True)
    telefono2 = models.CharField(max_length=20, blank=True)
    domicilio = models.TextField(blank=True)
    ocupacion = models.CharField(max_length=100, blank=True)
    empresa = models.CharField(max_length=100, blank=True)
    direccion = models.TextField(blank=True)
    email = models.EmailField(blank=True)

    def __str__(self):
        return self.nombre

class DatosLaborales(models.Model):
    empresa = models.CharField(max_length=100)
    direccion = models.TextField(blank=True)
    telefono1 = models.CharField(max_length=20, blank=True)
    telefono2 = models.CharField(max_length=20, blank=True)
    ocupacion = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.empresa

class DatosSeguro(models.Model):
    aseguradora = models.CharField(max_length=100)
    lista_precios = models.CharField(max_length=100)
    carnet = models.CharField(max_length=50, blank=True)
    certificado = models.CharField(max_length=50, blank=True)
    nombre_titular = models.CharField(max_length=100, blank=True)
    coaseguro = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    valor_copago = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    valor_deducible = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return self.aseguradora

class GarantiaPago(models.Model):
    tipo = models.CharField(max_length=100)
    numero_tc_cheque = models.CharField(max_length=50, blank=True)
    nit = models.CharField(max_length=20, blank=True)
    nombre_factura = models.CharField(max_length=100, blank=True)
    direccion_factura = models.TextField(blank=True)
    correo_factura = models.EmailField(blank=True)

    def __str__(self):
        return self.tipo

class Admision(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    acompanante = models.ForeignKey(Acompanante, on_delete=models.SET_NULL, null=True, blank=True)
    responsable = models.ForeignKey(Responsable, on_delete=models.SET_NULL, null=True, blank=True)
    esposo = models.ForeignKey(Esposo, on_delete=models.SET_NULL, null=True, blank=True)
    datos_laborales = models.ForeignKey(DatosLaborales, on_delete=models.SET_NULL, null=True, blank=True)
    datos_seguro = models.ForeignKey(DatosSeguro, on_delete=models.SET_NULL, null=True, blank=True)
    garantia_pago = models.ForeignKey(GarantiaPago, on_delete=models.SET_NULL, null=True, blank=True)
    area_admision = models.CharField(max_length=100)
    habitacion = models.CharField(max_length=50)
    medico_tratante = models.CharField(max_length=100)
    fecha = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Admisión de {self.paciente.nombre} ({self.fecha})"
