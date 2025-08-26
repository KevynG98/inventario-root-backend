from rest_framework import serializers
from decimal import Decimal, ROUND_HALF_UP
from ..models.salidasModel import Salida, SalidaItem


def _q2(val):
    try:
        return Decimal(str(val)).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
    except Exception:
        return Decimal('0.00')


class SalidaItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = SalidaItem
        exclude = ['salida']

    def validate(self, attrs):
        attrs = super().validate(attrs)
        for k in ('costo', 'cantidad', 'precio_sin_iva', 'iva', 'total'):
            if k in attrs:
                attrs[k] = _q2(attrs[k])
        return attrs


class SalidaSerializer(serializers.ModelSerializer):
    items = SalidaItemSerializer(many=True, required=False)

    class Meta:
        model = Salida
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at', 'usuario', 'aplicado_por')
