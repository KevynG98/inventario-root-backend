import json
from ..models.historialApiModel import HistorialAPI

class AuditoriaMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        cuerpo = b''
        data = {}

        try:
            if request.method in ['POST', 'PUT', 'DELETE'] and not any(request.path.startswith(p) for p in ['/admin', '/static']):
                # ✅ Leer y guardar el body sin consumir el stream
                cuerpo = request.body
                request._body = cuerpo  # Reasignar para que views puedan acceder

                try:
                    data = json.loads(cuerpo.decode('utf-8') or '{}')
                except:
                    data = {}

        except Exception as e:
            print(f"❌ Error leyendo cuerpo en AuditoriaMiddleware: {e}")

        # Ejecutar la vista
        response = self.get_response(request)

        try:
            metodo = request.method.upper()
            path = request.path
            usuario = getattr(request, 'user', None)
            status_code = response.status_code
            respuesta = response.content.decode('utf-8') if response.content else ''
            exito = 200 <= status_code < 400
            descripcion = getattr(request, 'descripcion', None)

            if metodo in ['POST', 'PUT', 'DELETE'] and not any(path.startswith(p) for p in ['/admin', '/static']):
                # Descripción por defecto si no se definió
                if not descripcion:
                    if path.startswith('/user/') and metodo == 'POST':
                        descripcion = f"Se creó el usuario '{data.get('nombre', 'N/A')}'"
                    elif path.startswith('/user/') and metodo == 'PUT':
                        descripcion = f"Se actualizó un usuario"
                    elif path.startswith('/user/') and metodo == 'DELETE':
                        descripcion = f"Se eliminó el usuario con ID {path.rstrip('/').split('/')[-1]}"

                    elif path.startswith('/habitaciones/') and metodo == 'POST':
                        descripcion = f"Se creó la habitación '{data.get('codigo', 'N/A')}'"
                    elif path.startswith('/habitaciones/') and metodo == 'PUT':
                        descripcion = f"Se actualizó la habitación '{data.get('codigo', 'N/A')}'"
                    elif path.startswith('/habitaciones/') and metodo == 'DELETE':
                        descripcion = f"Se eliminó la habitación con ID {path.rstrip('/').split('/')[-1]}"

                    elif path.startswith('/admisiones/') and metodo == 'POST':
                        descripcion = "Se creó una nueva admisión"
                    elif path.startswith('/admisiones/') and metodo == 'PUT':
                        descripcion = "Se actualizó una admisión"
                    elif path.startswith('/admisiones/') and metodo == 'DELETE':
                        descripcion = f"Se eliminó la admisión con ID {path.rstrip('/').split('/')[-1]}"

                    elif path.startswith('/inventario/marcas') and metodo == 'POST':
                        descripcion = f"Se creó una marca llamada '{data.get('nombre', 'N/A')}'"
                    elif path.startswith('/inventario/marcas') and metodo == 'PUT':
                        descripcion = f"Se actualizó una marca"
                    elif path.startswith('/inventario/marcas') and metodo == 'DELETE':
                        descripcion = f"Se eliminó una marca con ID {path.rstrip('/').split('/')[-1]}"

                    elif path.startswith('/inventario/proveedores') and metodo == 'POST':
                        descripcion = f"Se creó un proveedor '{data.get('nombre', 'N/A')}'"
                    elif path.startswith('/inventario/proveedores') and metodo == 'PUT':
                        descripcion = f"Se actualizó un proveedor"
                    elif path.startswith('/inventario/proveedores') and metodo == 'DELETE':
                        descripcion = f"Se eliminó un proveedor con ID {path.rstrip('/').split('/')[-1]}"

                    elif path.startswith('/inventario/categorias') and metodo == 'POST':
                        descripcion = f"Se creó una categoría '{data.get('nombre', 'N/A')}'"
                    elif path.startswith('/inventario/categorias') and metodo == 'PUT':
                        descripcion = f"Se actualizó una categoría"
                    elif path.startswith('/inventario/categorias') and metodo == 'DELETE':
                        descripcion = f"Se eliminó una categoría con ID {path.rstrip('/').split('/')[-1]}"
                    
                    elif path.startswith('/inventario/bodegas-crear') and metodo == 'POST':
                        descripcion = f"Se creó una bodega '{data.get('nombre', 'N/A')}'"
                    elif path.startswith('/inventario/bodegas-actualizar') and metodo == 'PUT':
                        descripcion = f"Se actualizó una bodega"
                    elif path.startswith('/inventario/bodegas-eliminar') and metodo == 'DELETE':
                        descripcion = f"Se eliminó una bodega con ID {path.rstrip('/').split('/')[-1]}"
                        
                    # SKUs
                    elif path.startswith('/inventario/skus-crear') and metodo == 'POST':
                        descripcion = f"Se creó un SKU con código '{data.get('codigo_sku', 'N/A')}'"

                    elif path.startswith('/inventario/skus-actualizar') and metodo == 'PUT':
                        descripcion = f"Se actualizó el SKU con ID {path.rstrip('/').split('/')[-1]}"

                    elif path.startswith('/inventario/skus-eliminar') and metodo == 'DELETE':
                        descripcion = f"Se eliminó el SKU con ID {path.rstrip('/').split('/')[-1]}"

                    # Movimiento de productos entre bodegas
                    elif path.startswith('/inventario/skus/mover/') and metodo == 'POST':
                        from api.models import InventarioSKU  # importa el modelo si no está arriba

                        sku_id = data.get('sku')
                        nombre_sku = 'N/A'
                        try:
                            nombre_sku = InventarioSKU.objects.get(id=sku_id).nombre
                        except InventarioSKU.DoesNotExist:
                            pass

                        descripcion = (
                            f"Se movieron {data.get('cantidad', 0)} unidades del producto '{nombre_sku}' "
                            f"de '{data.get('bodega_origen', 'N/A')}' a '{data.get('bodega_destino', 'N/A')}'"
                        )



                # Guardar el historial
                HistorialAPI.objects.create(
                    metodo=metodo,
                    endpoint=path,
                    usuario=usuario if usuario and usuario.is_authenticated else None,
                    cuerpo=cuerpo.decode('utf-8') if cuerpo else '',
                    descripcion=descripcion,
                    exito=exito,
                    codigo_respuesta=status_code,
                    respuesta=respuesta
                )

        except Exception as e:
            print(f"❌ Error en AuditoriaMiddleware: {e}")

        return response
