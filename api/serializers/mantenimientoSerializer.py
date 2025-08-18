from rest_framework import serializers
from ..models.mantenimientoModel import CentroCosto, Departamento, CuentaContable


class CentroCostoSerializer(serializers.ModelSerializer):
    class Meta:
        model = CentroCosto
        fields = '__all__'

    def validate(self, attrs):
        nombre = attrs.get('nombre')
        if nombre:
            qs = CentroCosto.objects.filter(is_active=True, nombre__iexact=nombre)
            if self.instance:
                qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                raise serializers.ValidationError({'nombre': 'Ya existe un Centro de Costo con ese nombre.'})
        return attrs


class DepartamentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Departamento
        fields = '__all__'

    def validate(self, attrs):
        nombre = attrs.get('nombre')
        if nombre:
            qs = Departamento.objects.filter(is_active=True, nombre__iexact=nombre)
            if self.instance:
                qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                raise serializers.ValidationError({'nombre': 'Ya existe un Departamento con ese nombre.'})
        return attrs


class CuentaContableSerializer(serializers.ModelSerializer):
    class Meta:
        model = CuentaContable
        fields = '__all__'

    def validate(self, attrs):
        nombre = attrs.get('nombre')
        if nombre:
            qs = CuentaContable.objects.filter(is_active=True, nombre__iexact=nombre)
            if self.instance:
                qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                raise serializers.ValidationError({'nombre': 'Ya existe una Cuenta Contable con ese nombre.'})
        return attrs
