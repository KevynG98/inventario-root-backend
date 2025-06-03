from rest_framework.pagination import PageNumberPagination

class CustomPageNumberPagination(PageNumberPagination):
    page_size = 5  # Valor por defecto
    page_size_query_param = 'page_size'  # Para usar ?page_size=15
    max_page_size = 1000  # Para limitar abuso
