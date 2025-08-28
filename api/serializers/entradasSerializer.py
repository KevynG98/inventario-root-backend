from rest_framework import serializers
from ..models.entradasModel import Entrada, EntradaItem
from decimal import Decimal, ROUND_HALF_UP

def _q2(val):
    try:
        return Decimal(str(val)).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
    except Exception:
        # Si viene vacío o None
        return Decimal('0.00')


class EntradaItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = EntradaItem
        exclude = ['entrada']

    def validate(self, attrs):
        attrs = super().validate(attrs)
        # Normalizar a 2 decimales para cumplir max_digits/decimal_places en SQL Server
        if 'costo' in attrs:
            attrs['costo'] = _q2(attrs.get('costo'))
        if 'cantidad' in attrs:
            attrs['cantidad'] = _q2(attrs.get('cantidad'))
        if 'precio_sin_iva' in attrs:
            attrs['precio_sin_iva'] = _q2(attrs.get('precio_sin_iva'))
        if 'iva' in attrs:
            attrs['iva'] = _q2(attrs.get('iva'))
        if 'total' in attrs:
            attrs['total'] = _q2(attrs.get('total'))
        return attrs


class EntradaSerializer(serializers.ModelSerializer):
    items = EntradaItemSerializer(many=True, required=False)
    total = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Entrada
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at', 'estado', 'usuario', 'aplicado_por', 'total')

    def get_total(self, obj):
        try:
            items = getattr(obj, 'items', None)
            if items is None:
                return '0.00'
            from decimal import Decimal
            total = sum([(it.total or 0) for it in items.all()])
            return f"{Decimal(total):.2f}"
        except Exception:
            return '0.00'

    def create(self, validated_data):
        items_data = validated_data.pop('items', [])
        request = self.context.get('request') if self.context else None
        user = request.user if request else None
        username = None
        if user and getattr(user, 'is_authenticated', False):
            username = user.username
        elif request:
            username = request.headers.get('X-User') or None
        entrada = Entrada.objects.create(usuario=username, **validated_data)
        for item in items_data:
            item = EntradaItemSerializer().to_internal_value(item)
            EntradaItem.objects.create(entrada=entrada, **item)
        return entrada

    def update(self, instance, validated_data):
        # Solo permitir actualizar si no está aplicada
        if instance.estado == 'aplicada':
            raise serializers.ValidationError({'estado': 'No se puede editar una entrada aplicada.'})

        items_data = validated_data.pop('items', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if items_data is not None:
            # Reemplazar items: borrar existentes y recrear
            instance.items.all().delete()
            for item in items_data:
                item = EntradaItemSerializer().to_internal_value(item)
                EntradaItem.objects.create(entrada=instance, **item)

        return instance
