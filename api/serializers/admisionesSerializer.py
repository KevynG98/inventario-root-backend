from rest_framework import serializers
from django.db.models import Max
from ..models.admisionesModel import (
    Paciente, Acompanante, Responsable, Esposo,
    DatosLaborales, DatosSeguro, GarantiaPago, Admision,
    MovimientoCuenta
)

# 🔹 Serializers simples para cada modelo
class PacienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Paciente
        fields = '__all__'

class AcompananteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Acompanante
        fields = '__all__'

class ResponsableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Responsable
        fields = '__all__'

class EsposoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Esposo
        fields = '__all__'

class DatosLaboralesSerializer(serializers.ModelSerializer):
    class Meta:
        model = DatosLaborales
        fields = '__all__'

class DatosSeguroSerializer(serializers.ModelSerializer):
    class Meta:
        model = DatosSeguro
        fields = '__all__'

class GarantiaPagoSerializer(serializers.ModelSerializer):
    class Meta:
        model = GarantiaPago
        fields = '__all__'


# 🔹 Para detalle (GET)
class AdmisionDetalleSerializer(serializers.ModelSerializer):
    paciente = PacienteSerializer()
    acompanante = AcompananteSerializer()
    responsable = ResponsableSerializer()
    esposo = EsposoSerializer()
    datos_laborales = DatosLaboralesSerializer()
    datos_seguro = DatosSeguroSerializer()
    garantia_pago = GarantiaPagoSerializer()

    class Meta:
        model = Admision
        fields = '__all__'


# 🔹 Para creación (POST) desde datos planos
class AdmisionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Admision
        fields = ['area_admision', 'habitacion', 'medico_tratante']

    def create(self, validated_data):
        request_data = self.context['request'].data

        paciente = Paciente.objects.create(
            primer_nombre=request_data.get('p_primer_nombre'),
            segundo_nombre=request_data.get('p_segundo_nombre'),
            primer_apellido=request_data.get('p_primer_apellido'),
            segundo_apellido=request_data.get('p_segundo_apellido'),
            apellido_casada=request_data.get('p_apellido_casada'),
            genero=request_data.get('p_genero'),
            estado_civil=request_data.get('p_estado_civil'),
            fecha_nacimiento=request_data.get('p_fecha_nacimiento'),
            edad=request_data.get('edad'),
            tipo_identificacion=request_data.get('p_tipo_identificacion'),
            numero_identificacion=request_data.get('p_numero_identificacion'),
            telefono=request_data.get('p_telefono'),
            direccion=request_data.get('direccion'),
            telefono1=request_data.get('telefono1'),
            telefono2=request_data.get('telefono2'),
            correo=request_data.get('correo'),
            observacion=request_data.get('observacion'),
            religion=request_data.get('religion'),
            nit=request_data.get('nit'),
            nombre_factura=request_data.get('nombreFactura'),
            direccion_factura=request_data.get('direccionFactura'),
            correo_factura=request_data.get('correoFactura'),
        )

        acompanante = Acompanante.objects.create(
            nombre=request_data.get('acompananteNombre'),
            telefono=request_data.get('acompananteTelefono')
        )

        responsable = Responsable.objects.create(
            primer_nombre=request_data.get('responsablePrimerNombre'),
            segundo_nombre=request_data.get('responsableSegundoNombre'),
            primer_apellido=request_data.get('responsablePrimerApellido'),
            segundo_apellido=request_data.get('responsableSegundoApellido'),
            tipo_identificacion=request_data.get('responsableTipoIdentificacion'),
            numero_identificacion=request_data.get('responsableNumeroIdentificacion'),
            fecha_nacimiento=request_data.get('responsableFechaNacimiento'),
            edad=request_data.get('responsableEdad'),
            genero=request_data.get('responsableGenero'),
            relacion_paciente=request_data.get('responsableRelacionPaciente'),
            ocupacion=request_data.get('responsableOcupacion'),
            domicilio=request_data.get('responsableDomicilio'),
            empresa=request_data.get('responsableEmpresa'),
            direccion=request_data.get('responsableDireccion'),
            telefono1=request_data.get('responsableTelefono1'),
            telefono2=request_data.get('responsableTelefono2'),
            contacto=request_data.get('responsableContacto'),
            email=request_data.get('responsableEmail')
        )

        esposo = Esposo.objects.create(
            nombre=request_data.get('esposoNombre'),
            genero=request_data.get('esposoGenero'),
            tipo_identificacion=request_data.get('esposoTipoIdentificacion'),
            numero_identificacion=request_data.get('esposoNumeroIdentificacion'),
            fecha_nacimiento=request_data.get('esposoFechaNacimiento'),
            edad=request_data.get('esposoEdad'),
            telefono1=request_data.get('esposoTelefono1'),
            telefono2=request_data.get('esposoTelefono2'),
            domicilio=request_data.get('esposoDomicilio'),
            ocupacion=request_data.get('esposoOcupacion'),
            empresa=request_data.get('esposoEmpresa'),
            direccion=request_data.get('esposoDireccion'),
            email=request_data.get('esposoEmail')
        )

        datos_laborales = DatosLaborales.objects.create(
            empresa=request_data.get('empresa'),
            direccion=request_data.get('direccionEmpresa'),
            telefono1=request_data.get('telefonoEmpresa1'),
            telefono2=request_data.get('telefonoEmpresa2'),
            ocupacion=request_data.get('ocupacion')
        )

        datos_seguro = DatosSeguro.objects.create(
            aseguradora=request_data.get('aseguradora'),
            lista_precios=request_data.get('listaPrecios'),
            carnet=request_data.get('carnet'),
            certificado=request_data.get('certificado'),
            nombre_titular=request_data.get('nombreTitular'),
            coaseguro=request_data.get('coaseguro'),
            valor_copago=request_data.get('valorCopago'),
            valor_deducible=request_data.get('valorDeducible')
        )

        garantia_pago = GarantiaPago.objects.create(
            tipo=request_data.get('tipoGarantia'),
            numero_tc_cheque=request_data.get('numeroTcCheque'),
            nit=request_data.get('nit'),
            nombre_factura=request_data.get('nombreFactura'),
            direccion_factura=request_data.get('direccionFactura'),
            correo_factura=request_data.get('correoFactura')
        )
        
        estado = validated_data.pop('estado', 'ingresado') 
        
        ultimo_id = Admision.objects.aggregate(Max('id'))['id__max']
        nuevo_id = max(7000, (ultimo_id or 6999) + 1)
        
        admision = Admision.objects.create(
            id=nuevo_id,
            paciente=paciente,
            acompanante=acompanante,
            responsable=responsable,
            esposo=esposo,
            datos_laborales=datos_laborales,
            datos_seguro=datos_seguro,
            garantia_pago=garantia_pago,
            estado=estado,
            **validated_data
        )

        return admision


# 🔹 Para actualización (PUT) — espera datos anidados

class AdmisionUpdateFlatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Admision
        fields = ['area_admision', 'habitacion', 'medico_tratante']

    def update(self, instance, validated_data):
        data = self.context['request'].data

        def actualizar_si_existe(obj, field, data, key):
            if key in data and data[key] is not None:
                setattr(obj, field, data[key])

        # Paciente
        paciente = instance.paciente
        actualizar_si_existe(paciente, 'primer_nombre', data, 'p_primer_nombre')
        actualizar_si_existe(paciente, 'segundo_nombre', data, 'p_segundo_nombre')
        actualizar_si_existe(paciente, 'primer_apellido', data, 'p_primer_apellido')
        actualizar_si_existe(paciente, 'segundo_apellido', data, 'p_segundo_apellido')
        actualizar_si_existe(paciente, 'apellido_casada', data, 'p_apellido_casada')
        actualizar_si_existe(paciente, 'genero', data, 'p_genero')
        actualizar_si_existe(paciente, 'estado_civil', data, 'p_estado_civil')
        actualizar_si_existe(paciente, 'fecha_nacimiento', data, 'p_fecha_nacimiento')
        actualizar_si_existe(paciente, 'edad', data, 'edad')
        actualizar_si_existe(paciente, 'tipo_identificacion', data, 'p_tipo_identificacion')
        actualizar_si_existe(paciente, 'numero_identificacion', data, 'p_numero_identificacion')
        actualizar_si_existe(paciente, 'telefono', data, 'p_telefono')
        actualizar_si_existe(paciente, 'direccion', data, 'direccion')
        actualizar_si_existe(paciente, 'telefono1', data, 'telefono1')
        actualizar_si_existe(paciente, 'telefono2', data, 'telefono2')
        actualizar_si_existe(paciente, 'correo', data, 'correo')
        actualizar_si_existe(paciente, 'observacion', data, 'observacion')
        actualizar_si_existe(paciente, 'religion', data, 'religion')
        actualizar_si_existe(paciente, 'nit', data, 'nit')
        actualizar_si_existe(paciente, 'nombre_factura', data, 'nombreFactura')
        actualizar_si_existe(paciente, 'direccion_factura', data, 'direccionFactura')
        actualizar_si_existe(paciente, 'correo_factura', data, 'correoFactura')
        paciente.save()

        # Acompañante
        if instance.acompanante:
            actualizar_si_existe(instance.acompanante, 'nombre', data, 'acompananteNombre')
            actualizar_si_existe(instance.acompanante, 'telefono', data, 'acompananteTelefono')
            instance.acompanante.save()

        # Responsable
        if instance.responsable:
            r = instance.responsable
            actualizar_si_existe(r, 'primer_nombre', data, 'responsablePrimerNombre')
            actualizar_si_existe(r, 'segundo_nombre', data, 'responsableSegundoNombre')
            actualizar_si_existe(r, 'primer_apellido', data, 'responsablePrimerApellido')
            actualizar_si_existe(r, 'segundo_apellido', data, 'responsableSegundoApellido')
            actualizar_si_existe(r, 'tipo_identificacion', data, 'responsableTipoIdentificacion')
            actualizar_si_existe(r, 'numero_identificacion', data, 'responsableNumeroIdentificacion')
            actualizar_si_existe(r, 'fecha_nacimiento', data, 'responsableFechaNacimiento')
            actualizar_si_existe(r, 'edad', data, 'responsableEdad')
            actualizar_si_existe(r, 'genero', data, 'responsableGenero')
            actualizar_si_existe(r, 'relacion_paciente', data, 'responsableRelacionPaciente')
            actualizar_si_existe(r, 'ocupacion', data, 'responsableOcupacion')
            actualizar_si_existe(r, 'domicilio', data, 'responsableDomicilio')
            actualizar_si_existe(r, 'empresa', data, 'responsableEmpresa')
            actualizar_si_existe(r, 'direccion', data, 'responsableDireccion')
            actualizar_si_existe(r, 'telefono1', data, 'responsableTelefono1')
            actualizar_si_existe(r, 'telefono2', data, 'responsableTelefono2')
            actualizar_si_existe(r, 'contacto', data, 'responsableContacto')
            actualizar_si_existe(r, 'email', data, 'responsableEmail')
            r.save()

        # Esposo
        if instance.esposo:
            e = instance.esposo
            actualizar_si_existe(e, 'nombre', data, 'esposoNombre')
            actualizar_si_existe(e, 'genero', data, 'esposoGenero')
            actualizar_si_existe(e, 'tipo_identificacion', data, 'esposoTipoIdentificacion')
            actualizar_si_existe(e, 'numero_identificacion', data, 'esposoNumeroIdentificacion')
            actualizar_si_existe(e, 'fecha_nacimiento', data, 'esposoFechaNacimiento')
            actualizar_si_existe(e, 'edad', data, 'esposoEdad')
            actualizar_si_existe(e, 'telefono1', data, 'esposoTelefono1')
            actualizar_si_existe(e, 'telefono2', data, 'esposoTelefono2')
            actualizar_si_existe(e, 'domicilio', data, 'esposoDomicilio')
            actualizar_si_existe(e, 'ocupacion', data, 'esposoOcupacion')
            actualizar_si_existe(e, 'empresa', data, 'esposoEmpresa')
            actualizar_si_existe(e, 'direccion', data, 'esposoDireccion')
            actualizar_si_existe(e, 'email', data, 'esposoEmail')
            e.save()

        # Datos laborales
        if instance.datos_laborales:
            d = instance.datos_laborales
            actualizar_si_existe(d, 'empresa', data, 'empresa')
            actualizar_si_existe(d, 'direccion', data, 'direccionEmpresa')
            actualizar_si_existe(d, 'telefono1', data, 'telefonoEmpresa1')
            actualizar_si_existe(d, 'telefono2', data, 'telefonoEmpresa2')
            actualizar_si_existe(d, 'ocupacion', data, 'ocupacion')
            d.save()

        # Datos del seguro
        if instance.datos_seguro:
            s = instance.datos_seguro
            actualizar_si_existe(s, 'aseguradora', data, 'aseguradora')
            actualizar_si_existe(s, 'lista_precios', data, 'listaPrecios')
            actualizar_si_existe(s, 'carnet', data, 'carnet')
            actualizar_si_existe(s, 'certificado', data, 'certificado')
            actualizar_si_existe(s, 'nombre_titular', data, 'nombreTitular')
            actualizar_si_existe(s, 'coaseguro', data, 'coaseguro')
            actualizar_si_existe(s, 'valor_copago', data, 'valorCopago')
            actualizar_si_existe(s, 'valor_deducible', data, 'valorDeducible')
            s.save()

        # Garantía de pago
        if instance.garantia_pago:
            g = instance.garantia_pago
            actualizar_si_existe(g, 'tipo', data, 'tipoGarantia')
            actualizar_si_existe(g, 'numero_tc_cheque', data, 'numeroTcCheque')
            actualizar_si_existe(g, 'nit', data, 'nit')
            actualizar_si_existe(g, 'nombre_factura', data, 'nombreFactura')
            actualizar_si_existe(g, 'direccion_factura', data, 'direccionFactura')
            actualizar_si_existe(g, 'correo_factura', data, 'correoFactura')
            g.save()

        # Campos propios de admisión
        actualizar_si_existe(instance, 'area_admision', data, 'area_admision')
        actualizar_si_existe(instance, 'habitacion', data, 'habitacion')
        actualizar_si_existe(instance, 'medico_tratante', data, 'medicoTratante')
        instance.save()
        return instance
class MovimientoCuentaSerializer(serializers.ModelSerializer):
     class Meta:
        model = MovimientoCuenta
        fields = [
            'id',
            'fecha',
            'categoria',
            'descripcion',
            'facturar_a',
            'cantidad',
            'precio_unitario',
            'total',
            'precio_aseguradora',
            'total_aseguradora',
            'precio_paciente',
            'total_paciente',
            'observacion',
            'admision'
        ]

class EstadoCuentaSerializer(serializers.ModelSerializer):
    paciente = serializers.SerializerMethodField()
    movimientos = MovimientoCuentaSerializer(many=True, read_only=True)

    class Meta:
        model = Admision
        fields = [
            'id',
            'fecha',
            'area_admision',
            'habitacion',
            'medico_tratante',
            'paciente',
            'movimientos'
        ]

    def get_paciente(self, obj):
        paciente = obj.paciente
        return {
            'nombre': f"{paciente.primer_nombre} {paciente.primer_apellido}",
            'genero': paciente.genero,
            'edad': paciente.edad
        }
