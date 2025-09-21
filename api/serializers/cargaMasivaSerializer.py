from rest_framework import serializers

from ..models.cargaMasivaModel import (
    CargaMasivaExistencia,
    CargaMasivaExistenciaItem,
    CargaMasivaPrecio,
    CargaMasivaPrecioItem,
)


class CargaMasivaExistenciaItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CargaMasivaExistenciaItem
        fields = (
            'id',
            'sku',
            'descripcion',
            'cantidad_cargada',
            'cantidad_anterior',
            'cantidad_resultante',
        )


class CargaMasivaExistenciaSerializer(serializers.ModelSerializer):
    items = CargaMasivaExistenciaItemSerializer(many=True, read_only=True)

    class Meta:
        model = CargaMasivaExistencia
        fields = (
            'id',
            'bodega',
            'usuario',
            'archivo_nombre',
            'created_at',
            'items',
        )


class CargaMasivaPrecioItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CargaMasivaPrecioItem
        fields = (
            'id',
            'sku',
            'descripcion',
            'precio_anterior',
            'precio_nuevo',
        )


class CargaMasivaPrecioSerializer(serializers.ModelSerializer):
    items = CargaMasivaPrecioItemSerializer(many=True, read_only=True)

    class Meta:
        model = CargaMasivaPrecio
        fields = (
            'id',
            'seguro',
            'usuario',
            'archivo_nombre',
            'created_at',
            'items',
        )
