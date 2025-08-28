from rest_framework import serializers
from ..models.requisisionesModel import (
    Requisicion,
    ProductoRequisicion,
    ServicioRequisicion
)


class ProductoRequisicionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductoRequisicion
        exclude = ['requisicion']  # Se excluye porque se añade manualmente


class ServicioRequisicionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServicioRequisicion
        exclude = ['requisicion']  # Igual que arriba


class RequisicionSerializer(serializers.ModelSerializer):
    productos = ProductoRequisicionSerializer(many=True, required=False)
    servicios = ServicioRequisicionSerializer(many=True, required=False)

    class Meta:
        model = Requisicion
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')
        extra_kwargs = {
            'prioridad': {'required': False, 'allow_null': True, 'allow_blank': True},
            'centro_costo': {'required': False, 'allow_null': True, 'allow_blank': True},
            'area_solicitante': {'required': False, 'allow_null': True, 'allow_blank': True},
            'tipo_requisicion': {'required': False, 'allow_null': True, 'allow_blank': True},
            'bodega': {'required': False, 'allow_null': True, 'allow_blank': True},
            'estado': {'required': False, 'allow_null': True, 'allow_blank': True},
        }

    def create(self, validated_data):
        productos_data = validated_data.pop('productos', [])
        servicios_data = validated_data.pop('servicios', [])

        requisicion = Requisicion.objects.create(**validated_data)

        for producto in productos_data:
            ProductoRequisicion.objects.create(requisicion=requisicion, **producto)

        for servicio in servicios_data:
            ServicioRequisicion.objects.create(requisicion=requisicion, **servicio)

        return requisicion

    def update(self, instance, validated_data):
        productos_data = validated_data.pop('productos', None)
        servicios_data = validated_data.pop('servicios', None)

        # Update simple fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Replace productos if provided
        if productos_data is not None:
            ProductoRequisicion.objects.filter(requisicion=instance).delete()
            for producto in productos_data:
                ProductoRequisicion.objects.create(requisicion=instance, **producto)

        # Replace servicios if provided
        if servicios_data is not None:
            ServicioRequisicion.objects.filter(requisicion=instance).delete()
            for servicio in servicios_data:
                ServicioRequisicion.objects.create(requisicion=instance, **servicio)

        return instance

class RequisicionEstadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Requisicion
        # Permit update of estado and description via estado endpoint
        fields = ('estado', 'descripcion', 'estado_actualizado_por')
        extra_kwargs = {
            'descripcion': {'required': False, 'allow_null': True, 'allow_blank': True},
            'estado_actualizado_por': {'read_only': True},
        }
