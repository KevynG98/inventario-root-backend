from rest_framework import serializers
from ..models.proyectoModel import Proyectos
from ..models.detalleProyectoModel import DetalleProyectos
from .detalleProyectoSerializer import DetalleProyectoSerializer
from api.views.contactEmailView import enviar_correo_nueva_cotizacion


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

        productos_resumen = []

        for p in productos_data:
            print("LISTADO DE PRODUCRO ", p)
            DetalleProyectos.objects.create(
                proyectoId=proyecto,
                productoId=p["productoId"],
                cantidadProducto=p["cantidadProducto"],
                productoSubTotal=p["productoSubTotal"],
            )

            # Construimos resumen para el correo: nombre del producto y cantidad solicitada
            producto_obj = p.get("productoId")
            cantidad = p.get("cantidadProducto")
            nombre_producto = getattr(producto_obj, "nombre", str(producto_obj)) if producto_obj else ""
            productos_resumen.append({
                "nombre": nombre_producto,
                "cantidad": cantidad,
            })

        # Enviar correo de "Nueva cotización" una vez creado el proyecto y sus productos
        try:
            enviar_correo_nueva_cotizacion(
                nombre_empresa=proyecto.nombreEmpresa,
                email_empresa=proyecto.emailEmpresa,
                telefono_empresa=proyecto.telefonoEmpresa,
                direccion=proyecto.direccionEmpresa,
                productos=productos_resumen,
            )
        except Exception:
            # No interrumpir la creación del proyecto si falla el envío de correo
            pass

        return proyecto
