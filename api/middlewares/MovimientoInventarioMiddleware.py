import json
from django.utils import timezone
from api.models import InventarioSKU, MovimientoHistorico

class MovimientoInventarioMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        self.body_data = {}
        try:
            if request.method in ['POST', 'PUT'] and request.path.startswith('/inventario/skus'):
                self.body_data = json.loads(request.body.decode('utf-8') or '{}')
        except:
            self.body_data = {}

        response = self.get_response(request)

        try:
            hoy = timezone.now().date()

            # ✅ CREAR SKU
            if request.method == 'POST' and request.path.startswith('/inventario/skus-crear'):
                sku_code = self.body_data.get('codigo_sku')
                sku = InventarioSKU.objects.get(codigo_sku=sku_code)
                cantidad = sum([b['cantidad'] for b in self.body_data.get('bodegas', [])])
                inventario_actual = sum([b.cantidad for b in sku.bodegas.all()])

                registro, creado = MovimientoHistorico.objects.get_or_create(
                    sku=sku, fecha=hoy,
                    defaults={
                        'inventario_inicial': inventario_actual - cantidad,
                        'inventario_final': inventario_actual
                    }
                )
                registro.orden_compra += cantidad
                registro.observaciones = (registro.observaciones or '') + f"\nCreación inicial con {cantidad} unidades"
                registro.inventario_final = inventario_actual
                registro.save()

            # ✅ MOVER PRODUCTO ENTRE BODEGAS
            elif request.method == 'POST' and request.path.startswith('/inventario/skus/mover'):
                sku_id = self.body_data.get('sku')
                cantidad = int(self.body_data.get('cantidad', 0))
                sku = InventarioSKU.objects.get(id=sku_id)
                inventario_actual = sum([b.cantidad for b in sku.bodegas.all()])

                registro, creado = MovimientoHistorico.objects.get_or_create(
                    sku=sku, fecha=hoy,
                    defaults={
                        'inventario_inicial': inventario_actual,
                        'inventario_final': inventario_actual
                    }
                )
                registro.traslado += cantidad
                registro.observaciones = (registro.observaciones or '') + (
                    f"\nTraslado de {cantidad} unidades de {self.body_data.get('bodega_origen')} "
                    f"a {self.body_data.get('bodega_destino')}"
                )
                registro.save()

            # ✅ ACTUALIZAR SKU
            elif request.method == 'PUT' and request.path.startswith('/inventario/skus-actualizar'):
                sku_id = int(request.path.rstrip('/').split('/')[-1])
                sku = InventarioSKU.objects.get(id=sku_id)
                inventario_actual = sum([b.cantidad for b in sku.bodegas.all()])

                registro, creado = MovimientoHistorico.objects.get_or_create(
                    sku=sku, fecha=hoy,
                    defaults={
                        'inventario_inicial': inventario_actual,
                        'inventario_final': inventario_actual
                    }
                )

                if not creado:
                    diferencia = inventario_actual - registro.inventario_final
                    if diferencia != 0:
                        signo = '+' if diferencia > 0 else ''
                        registro.observaciones = (registro.observaciones or '') + f"\nActualización del SKU (ajuste: {signo}{diferencia})"
                    else:
                        registro.observaciones = (registro.observaciones or '') + "\nActualización del SKU (sin cambios en stock)"
                    registro.inventario_final = inventario_actual
                else:
                    registro.observaciones = (registro.observaciones or '') + "\nActualización del SKU (primer cambio del día)"
                    registro.inventario_final = inventario_actual

                registro.save()



        except Exception as e:
            print("❌ Error en MovimientoInventarioMiddleware:", e)

        return response
