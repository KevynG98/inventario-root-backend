from rest_framework import serializers
from ..models.proyectoModel import Proyectos
from ..models.detalleProyectoModel import DetalleProyectos
from ..models.inventarioProductoModel import InventarioProducto


class DetalleProyectoSerializer(serializers.ModelSerializer):
    idProducto = serializers.PrimaryKeyRelatedField(
        queryset=InventarioProducto.objects.all(),
        source="productoId"
    )
    subTotal = serializers.DecimalField(
        max_digits=12, decimal_places=2, source="productoSubTotal"
    )

    class Meta:
        model = DetalleProyectos
        fields = ["idProducto", "subTotal"]
