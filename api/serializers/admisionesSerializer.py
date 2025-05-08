
from rest_framework import serializers
from ..models.admisionesModel import (
    Paciente, Acompanante, Responsable, Esposo,
    DatosLaborales, DatosSeguro, GarantiaPago, Admision,
    Habitacion
)

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

class AdmisionSerializer(serializers.ModelSerializer):
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

        admision = Admision.objects.create(
            paciente=paciente,
            acompanante=acompanante,
            responsable=responsable,
            esposo=esposo,
            datos_laborales=datos_laborales,
            datos_seguro=datos_seguro,
            garantia_pago=garantia_pago,
            **validated_data
        )

        return admision

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
        
class AdmisionSerializer(serializers.ModelSerializer):
    paciente = serializers.DictField()
    acompanante = serializers.DictField(required=False)
    responsable = serializers.DictField(required=False)
    esposo = serializers.DictField(required=False)
    datos_laborales = serializers.DictField(required=False)
    datos_seguro = serializers.DictField(required=False)
    garantia_pago = serializers.DictField(required=False)

    class Meta:
        model = Admision
        fields = '__all__'

    def update(self, instance, validated_data):
        # Paciente
        paciente_data = validated_data.pop('paciente')
        paciente, _ = Paciente.objects.update_or_create(id=instance.paciente.id, defaults=paciente_data)
        instance.paciente = paciente

        # Acompañante
        if 'acompanante' in validated_data:
            acompanante_data = validated_data.pop('acompanante')
            acompanante, _ = Acompanante.objects.update_or_create(
                id=instance.acompanante.id if instance.acompanante else None,
                defaults=acompanante_data
            )
            instance.acompanante = acompanante

        # Responsable
        if 'responsable' in validated_data:
            responsable_data = validated_data.pop('responsable')
            responsable, _ = Responsable.objects.update_or_create(
                id=instance.responsable.id if instance.responsable else None,
                defaults=responsable_data
            )
            instance.responsable = responsable

        # Esposo
        if 'esposo' in validated_data:
            esposo_data = validated_data.pop('esposo')
            esposo, _ = Esposo.objects.update_or_create(
                id=instance.esposo.id if instance.esposo else None,
                defaults=esposo_data
            )
            instance.esposo = esposo

        # Datos laborales
        if 'datos_laborales' in validated_data:
            laborales_data = validated_data.pop('datos_laborales')
            datos_laborales, _ = DatosLaborales.objects.update_or_create(
                id=instance.datos_laborales.id if instance.datos_laborales else None,
                defaults=laborales_data
            )
            instance.datos_laborales = datos_laborales

        # Datos seguro
        if 'datos_seguro' in validated_data:
            seguro_data = validated_data.pop('datos_seguro')
            datos_seguro, _ = DatosSeguro.objects.update_or_create(
                id=instance.datos_seguro.id if instance.datos_seguro else None,
                defaults=seguro_data
            )
            instance.datos_seguro = datos_seguro

        # Garantía de pago
        if 'garantia_pago' in validated_data:
            garantia_data = validated_data.pop('garantia_pago')
            garantia_pago, _ = GarantiaPago.objects.update_or_create(
                id=instance.garantia_pago.id if instance.garantia_pago else None,
                defaults=garantia_data
            )
            instance.garantia_pago = garantia_pago

        # Campos directos de admisión
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance
    
class HabitacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habitacion
        fields = ['id', 'codigo', 'area', 'estado', 'admision', 'paciente', 'nivel']