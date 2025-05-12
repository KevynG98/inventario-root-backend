
from django.db import models

class Paciente(models.Model):
    primer_nombre = models.CharField(max_length=100)
    segundo_nombre = models.CharField(max_length=100, blank=True, null=True)
    primer_apellido = models.CharField(max_length=100, blank=True, null=True)
    segundo_apellido = models.CharField(max_length=100, blank=True, null=True)
    apellido_casada = models.CharField(max_length=100, blank=True, null=True)

    genero = models.CharField(max_length=20)
    estado_civil = models.CharField(max_length=50)
    fecha_nacimiento = models.DateField()
    edad = models.IntegerField()

    tipo_identificacion = models.CharField(max_length=50)
    numero_identificacion = models.CharField(max_length=50)
    telefono = models.CharField(max_length=50, blank=True, null=True)

    # Datos adicionales (nuevos)
    direccion = models.CharField(max_length=200, blank=True, null=True)
    telefono1 = models.CharField(max_length=50, blank=True, null=True)
    telefono2 = models.CharField(max_length=50, blank=True, null=True)
    correo = models.EmailField(blank=True, null=True)
    observacion = models.TextField(blank=True, null=True)
    religion = models.CharField(max_length=50, blank=True, null=True)

    # Datos de facturación
    nit = models.CharField(max_length=50, blank=True, null=True)
    nombre_factura = models.CharField(max_length=150, blank=True, null=True)
    direccion_factura = models.CharField(max_length=200, blank=True, null=True)
    correo_factura = models.EmailField(blank=True, null=True)

    def __str__(self):
        return f"{self.primer_nombre} {self.primer_apellido}"

class Acompanante(models.Model):
    nombre = models.CharField(max_length=100, blank=True, null=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return self.nombre

class Responsable(models.Model):
    primer_nombre = models.CharField(max_length=50, blank=True, null=True)
    segundo_nombre = models.CharField(max_length=50, blank=True, null=True)
    primer_apellido = models.CharField(max_length=50, blank=True, null=True)
    segundo_apellido = models.CharField(max_length=50, blank=True, null=True)
    tipo_identificacion = models.CharField(max_length=50, blank=True, null=True)
    numero_identificacion = models.CharField(max_length=50, blank=True, null=True)
    fecha_nacimiento = models.DateField(null=True, blank=True)
    edad = models.IntegerField(null=True, blank=True)
    genero = models.CharField(max_length=20, blank=True, null=True)
    relacion_paciente = models.CharField(max_length=50, blank=True, null=True)
    ocupacion = models.CharField(max_length=100, blank=True, null=True)
    domicilio = models.TextField(blank=True, null=True)
    empresa = models.CharField(max_length=100, blank=True, null=True)
    direccion = models.TextField(blank=True, null=True)
    telefono1 = models.CharField(max_length=20, blank=True, null=True)
    telefono2 = models.CharField(max_length=20, blank=True, null=True)
    contacto = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)

    def __str__(self):
        return f"{self.primer_nombre} {self.primer_apellido}"

class Esposo(models.Model):
    nombre = models.CharField(max_length=100, blank=True, null=True)
    genero = models.CharField(max_length=20, blank=True, null=True)
    tipo_identificacion = models.CharField(max_length=50, blank=True, null=True)
    numero_identificacion = models.CharField(max_length=50, blank=True, null=True)
    fecha_nacimiento = models.DateField(null=True, blank=True)
    edad = models.IntegerField(null=True, blank=True)
    telefono1 = models.CharField(max_length=20, blank=True, null=True)
    telefono2 = models.CharField(max_length=20, blank=True, null=True)
    domicilio = models.TextField(blank=True, null=True)
    ocupacion = models.CharField(max_length=100, blank=True, null=True)
    empresa = models.CharField(max_length=100, blank=True, null=True)
    direccion = models.TextField(blank=True, null=True)
    email = models.EmailField(blank=True, null=True)

    def __str__(self):
        return self.nombre

class DatosLaborales(models.Model):
    empresa = models.CharField(max_length=100, blank=True, null=True)
    direccion = models.TextField(blank=True, null=True)
    telefono1 = models.CharField(max_length=20, blank=True, null=True)
    telefono2 = models.CharField(max_length=20, blank=True, null=True)
    ocupacion = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.empresa

class DatosSeguro(models.Model):
    aseguradora = models.CharField(max_length=100, blank=True, null=True)
    lista_precios = models.CharField(max_length=100, blank=True, null=True)
    carnet = models.CharField(max_length=50, blank=True, null=True)
    certificado = models.CharField(max_length=50, blank=True, null=True)
    nombre_titular = models.CharField(max_length=100, blank=True, null=True)
    coaseguro = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    valor_copago = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    valor_deducible = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return self.aseguradora

class GarantiaPago(models.Model):
    tipo = models.CharField(max_length=100, blank=True, null=True)
    numero_tc_cheque = models.CharField(max_length=50, blank=True, null=True)
    nit = models.CharField(max_length=20, blank=True, null=True)
    nombre_factura = models.CharField(max_length=100, blank=True, null=True)
    direccion_factura = models.TextField(blank=True, null=True)
    correo_factura = models.EmailField(blank=True, null=True)

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
    area_admision = models.CharField(max_length=100, blank=True, null=True)
    habitacion = models.CharField(max_length=50, blank=True, null=True)
    medico_tratante = models.CharField(max_length=100, blank=True, null=True)
    fecha = models.DateField(auto_now_add=True, blank=True, null=True)
    estado = models.CharField(
    max_length=20,
    choices=[
        ('ingresado', 'Ingresado'),
        ('listo_egreso', 'Listo para egreso'),
        ('egresado', 'Egresado'),
    ],
    default='ingresado'
)


    def __str__(self):
        return f"Admisión de {self.paciente.primer_nombre} {self.paciente.primer_apellido} ({self.fecha})"

class Habitacion(models.Model):
    codigo = models.CharField(max_length=10)
    area = models.CharField(max_length=100)
    estado = models.CharField(max_length=100)
    admision = models.IntegerField()
    paciente = models.CharField(max_length=200, null=True, blank=True)  # solo el nombre o identificador
    nivel = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.codigo} - {self.area}"
    
class MovimientoCuenta(models.Model):
    admision = models.ForeignKey(Admision, on_delete=models.CASCADE, related_name='movimientos')
    fecha = models.DateField(auto_now_add=True)
    categoria = models.CharField(max_length=100)
    descripcion = models.TextField()
    facturar_a = models.CharField(max_length=100, blank=True, null=True)

    cantidad = models.PositiveIntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    total = models.DecimalField(max_digits=12, decimal_places=2)

    precio_aseguradora = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    total_aseguradora = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)

    precio_paciente = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    total_paciente = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)

    observacion = models.TextField(blank=True, null=True)
