from rest_framework import serializers
from ..models.proyectoModel import Proyectos
from ..models.detalleProyectoModel import DetalleProyectos
from .detalleProyectoSerializer import DetalleProyectoSerializer

class ProyectoSerializer(serializers.ModelSerializer):
    productos = DetalleProyectoSerializer(many=True, write_only=True)

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
            "productos"
        ]

    def create(self, validated_data):
        productos_data = validated_data.pop("productos", [])

        # Crear el proyecto
        proyecto = Proyectos.objects.create(**validated_data)

        # Crear los detalles del proyecto
        for p in productos_data:
            DetalleProyectos.objects.create(
                proyectoId=proyecto,
                productoId=p["productoId"],
                productoSubTotal=p["productoSubTotal"],
            )

        return proyecto