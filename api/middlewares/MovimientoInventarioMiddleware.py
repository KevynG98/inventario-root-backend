"""
Middleware sin efecto: el historial de movimientos ya no se usa en la API reducida.
Se deja la clase para no romper referencias, pero no realiza acciones.
"""

class MovimientoInventarioMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response
