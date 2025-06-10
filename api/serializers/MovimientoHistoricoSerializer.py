from rest_framework import serializers
from ..models.movimientoHistoricoModel import MovimientoHistorico

class MovimientoHistoricoSerializer(serializers.ModelSerializer):
    sku_codigo = serializers.CharField(source='sku.codigo_sku', read_only=True)
    sku_nombre = serializers.CharField(source='sku.nombre', read_only=True)

    class Meta:
        model = MovimientoHistorico
        fields = '__all__'
