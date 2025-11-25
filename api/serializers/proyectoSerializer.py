from rest_framework import serializers
from ..models.proyectoModel import Proyectos
from ..models.detalleProyectoModel import DetalleProyectos
from .detalleProyectoSerializer import DetalleProyectoSerializer


class ProyectoSerializer(serializers.ModelSerializer):
    productos = DetalleProyectoSerializer(many=True, write_only=True)

    # 🔥 Campo SOLO DE LECTURA para retornar productos del proyecto
    productos_detalle = DetalleProyectoSerializer(source="detalles", many=True, read_only=True)

    class Meta:
        model = Proyectos
        fields = [
            "id",
            "nombreEmpresa",
            "nombreProyecto",
            "direccionEmpresa",
            "telefonoEmpresa",
            "emailEmpresa",
            "totalPresupuestado",
            "estatusProyecto",
            "productos",           # para crear
            "productos_detalle",   # para listar
        ]

    def create(self, validated_data):
        productos_data = validated_data.pop("productos", [])

        proyecto = Proyectos.objects.create(**validated_data)

        for p in productos_data:
            print("LISTADO DE PRODUCRO ",p)
            DetalleProyectos.objects.create(
                proyectoId=proyecto,
                productoId=p["productoId"],
                cantidadProducto=p["cantidadProducto"],
                productoSubTotal=p["productoSubTotal"],
            )

        return proyecto
