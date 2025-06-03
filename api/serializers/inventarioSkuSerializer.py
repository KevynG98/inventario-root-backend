from rest_framework import serializers
from ..models.inventariosSkuModel import InventarioSKU, BodegaSKU, MovimientoBodega

class BodegaSKUSerializer(serializers.ModelSerializer):
    class Meta:
        model = BodegaSKU
        fields = ['nombre_bodega', 'cantidad']

class InventarioSKUSerializer(serializers.ModelSerializer):
    bodegas = BodegaSKUSerializer(many=True, required=False)

    class Meta:
        model = InventarioSKU
        fields = '__all__'

    def create(self, validated_data):
        bodegas_data = validated_data.pop('bodegas', [])
        sku = InventarioSKU.objects.create(**validated_data)
        for bodega in bodegas_data:
            BodegaSKU.objects.create(sku=sku, **bodega)
        return sku

    def update(self, instance, validated_data):
        bodegas_data = validated_data.pop('bodegas', None)

        # Actualizar campos normales del SKU
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Si vienen bodegas, reemplazarlas
        if bodegas_data is not None:
            instance.bodegas.all().delete()
            for bodega in bodegas_data:
                BodegaSKU.objects.create(sku=instance, **bodega)

        return instance

class MovimientoBodegaSerializer(serializers.ModelSerializer):
    class Meta:
        model = MovimientoBodega
        fields = '__all__'
