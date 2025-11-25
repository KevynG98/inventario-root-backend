from rest_framework import serializers
from ..models.proyectoModel import Proyectos
from ..models.detalleProyectoModel import DetalleProyectos
from ..models.inventarioProductoModel import InventarioProducto
from .inventarioProductoSerializer import InventarioProductoSerializer

class DetalleProyectoSerializer(serializers.ModelSerializer):
    idProducto = serializers.PrimaryKeyRelatedField(
        queryset=InventarioProducto.objects.all(),
        source="productoId"
    )
    nombreProducto = serializers.CharField(
        source="productoId.nombre",
        read_only=True
    )
    subTotal = serializers.DecimalField(
        max_digits=12, decimal_places=2, source="productoSubTotal"
    )
    
    cantidad = serializers.IntegerField(
        source="cantidadProducto"
    )

    class Meta:
        model = DetalleProyectos
        fields = ["idProducto", "nombreProducto", "cantidad", "subTotal"]
