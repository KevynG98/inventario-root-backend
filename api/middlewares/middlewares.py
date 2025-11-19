import json
from ..models.historialApiModel import HistorialAPI

# ✅ Limpiar datos sensibles antes de guardar
def limpiar_cuerpo(data):
    data_filtrado = dict(data)
    for clave in ['password', 'old_password', 'new_password', 'token']:
        if clave in data_filtrado:
            data_filtrado[clave] = '***'
    return data_filtrado

class AuditoriaMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        cuerpo = b''
        data = {}

        try:
            if request.method in ['POST', 'PUT', 'DELETE'] and not any(request.path.startswith(p) for p in ['/admin', '/static']):
                cuerpo = request.body
                request._body = cuerpo

                try:
                    data = json.loads(cuerpo.decode('utf-8') or '{}')
                except:
                    data = {}
        except Exception as e:
            print(f"❌ Error leyendo cuerpo en AuditoriaMiddleware: {e}")

        # Ejecutar vista
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
                if not descripcion:
                    print(f"📌 [DEBUG] Método: {metodo} | Ruta: {path}")

                    # Login / logout
                    if path == '/user/' and metodo == 'POST':
                        descripcion = f"🆕 Se creó el usuario '{data.get('username', data.get('nombre', 'N/A'))}'"
                    elif path == '/user/login/' and metodo == 'POST':
                        descripcion = f"🔐 Inicio de sesión con usuario '{data.get('username', 'N/A')}'"
                    elif path == '/user/logout/' and metodo == 'POST':
                        descripcion = f"🚪 Usuario {usuario.username if usuario else 'desconocido'} cerró sesión"

                    # Usuarios
                    elif path.startswith('/user/') and metodo == 'PUT':
                        descripcion = f"Se actualizó un usuario"
                    elif path.startswith('/user/') and metodo == 'DELETE':
                        descripcion = f"Se eliminó el usuario con ID {path.rstrip('/').split('/')[-1]}"

                    # Habitaciones
                    elif path.startswith('/habitaciones/') and metodo == 'POST':
                        descripcion = f"Se creó la habitación '{data.get('codigo', 'N/A')}'"
                    elif path.startswith('/habitaciones/') and metodo == 'PUT':
                        descripcion = f"Se actualizó la habitación '{data.get('codigo', 'N/A')}'"
                    elif path.startswith('/habitaciones/') and metodo == 'DELETE':
                        descripcion = f"Se eliminó la habitación con ID {path.rstrip('/').split('/')[-1]}"

                    # Admisiones
                    elif path.startswith('/admisiones/') and metodo == 'POST':
                        descripcion = "Se creó una nueva admisión"
                    elif path.startswith('/admisiones/') and metodo == 'PUT':
                        descripcion = "Se actualizó una admisión"
                    elif path.startswith('/admisiones/') and metodo == 'DELETE':
                        descripcion = f"Se eliminó la admisión con ID {path.rstrip('/').split('/')[-1]}"

                    # Marcas
                    elif path.startswith('/inventario/marcas') and metodo == 'POST':
                        descripcion = f"Se creó una marca llamada '{data.get('nombre', 'N/A')}'"
                    elif path.startswith('/inventario/marcas') and metodo == 'PUT':
                        descripcion = f"Se actualizó una marca"
                    elif path.startswith('/inventario/marcas') and metodo == 'DELETE':
                        descripcion = f"Se eliminó una marca con ID {path.rstrip('/').split('/')[-1]}"

                    # Proveedores
                    elif path.startswith('/inventario/proveedores') and metodo == 'POST':
                        descripcion = f"Se creó un proveedor '{data.get('nombre', 'N/A')}'"
                    elif path.startswith('/inventario/proveedores') and metodo == 'PUT':
                        descripcion = f"Se actualizó un proveedor"
                    elif path.startswith('/inventario/proveedores') and metodo == 'DELETE':
                        descripcion = f"Se eliminó un proveedor con ID {path.rstrip('/').split('/')[-1]}"

                    # Categorías
                    elif path.startswith('/inventario/categorias') and metodo == 'POST':
                        descripcion = f"Se creó una categoría '{data.get('nombre', 'N/A')}'"
                    elif path.startswith('/inventario/categorias') and metodo == 'PUT':
                        descripcion = f"Se actualizó una categoría"
                    elif path.startswith('/inventario/categorias') and metodo == 'DELETE':
                        descripcion = f"Se eliminó una categoría con ID {path.rstrip('/').split('/')[-1]}"

                    # Bodegas
                    elif path.startswith('/inventario/bodegas-crear') and metodo == 'POST':
                        descripcion = f"Se creó una bodega '{data.get('nombre', 'N/A')}'"
                    elif path.startswith('/inventario/bodegas-actualizar') and metodo == 'PUT':
                        descripcion = f"Se actualizó una bodega"
                    elif path.startswith('/inventario/bodegas-eliminar') and metodo == 'DELETE':
                        descripcion = f"Se eliminó una bodega con ID {path.rstrip('/').split('/')[-1]}"

                    # SKUs
                    elif path.startswith('/inventario/productos-crear') and metodo == 'POST':
                        descripcion = f"Se creó un SKU con código '{data.get('codigo_sku', 'N/A')}'"
                    elif path.startswith('/inventario/productos-actualizar') and metodo == 'PUT':
                        descripcion = f"Se actualizó el SKU con ID {path.rstrip('/').split('/')[-1]}"
                    elif path.startswith('/inventario/productos-eliminar') and metodo == 'DELETE':
                        descripcion = f"Se eliminó el SKU con ID {path.rstrip('/').split('/')[-1]}"

                    # Movimiento entre bodegas
                    elif path.startswith('/inventario/productos/mover/') and metodo == 'POST':
                        from api.models import InventarioSKU
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

                if descripcion:
                    HistorialAPI.objects.create(
                        metodo=metodo,
                        endpoint=path,
                        usuario=usuario if usuario and usuario.is_authenticated else None,
                        cuerpo=json.dumps(limpiar_cuerpo(data)) if data else '',
                        descripcion=descripcion,
                        exito=exito,
                        codigo_respuesta=status_code,
                        respuesta=respuesta
                    )

        except Exception as e:
            print(f"❌ Error en AuditoriaMiddleware: {e}")

        return response
