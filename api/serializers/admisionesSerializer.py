
from rest_framework import serializers
from ..models.admisionesModel import (
    Paciente, Acompanante, Responsable, Esposo,
    DatosLaborales, DatosSeguro, GarantiaPago, Admision
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

        request_data = self.context['request'].data

        paciente = Paciente.objects.create(
            nombre=request_data.get('nombre'),
            fecha_nacimiento=request_data.get('fechaNacimiento'),
            edad=request_data.get('edad'),
            direccion=request_data.get('direccion'),
            telefono1=request_data.get('telefono1'),
            telefono2=request_data.get('telefono2'),
            correo=request_data.get('correo'),
            observacion=request_data.get('observacion'),
            religion=request_data.get('religion'),
            tipo_identificacion=request_data.get('tipoIdentificacion'),
            numero_identificacion=request_data.get('numeroIdentificacion'),
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
