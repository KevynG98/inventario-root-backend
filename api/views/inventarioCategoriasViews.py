from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema

from api.utils.pagination import CustomPageNumberPagination
from ..models.inventarioCategoriasModel import CategoriaInventario, SubcategoriaInventario
from ..serializers.inventarioCategoriasSerializer import CategoriaSerializer, SubcategoriaSerializer


@swagger_auto_schema(method='get', tags=['Inventario - Categorías'], operation_description="Listar categorías activas con paginación")
@api_view(['GET'])
def listar_categorias(request):
    categorias = CategoriaInventario.objects.filter(is_active=True).order_by('id')
    paginator = CustomPageNumberPagination()
    result_page = paginator.paginate_queryset(categorias, request)
    serializer = CategoriaSerializer(result_page, many=True)
    return paginator.get_paginated_response(serializer.data)


@swagger_auto_schema(method='post', tags=['Inventario - Categorías'], operation_description="Crear una nueva categoría", request_body=CategoriaSerializer)
@api_view(['POST'])
def crear_categoria(request):
    serializer = CategoriaSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(method='put', tags=['Inventario - Categorías'], operation_description="Actualizar una categoría por ID", request_body=CategoriaSerializer)
@api_view(['PUT'])
def actualizar_categoria(request, pk):
    try:
        categoria = CategoriaInventario.objects.get(pk=pk)
    except CategoriaInventario.DoesNotExist:
        return Response({'error': 'Categoría no encontrada'}, status=status.HTTP_404_NOT_FOUND)

    serializer = CategoriaSerializer(categoria, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(method='delete', tags=['Inventario - Categorías'], operation_description="Eliminar (soft delete) una categoría por ID")
@api_view(['DELETE'])
def eliminar_categoria(request, pk):
    try:
        categoria = CategoriaInventario.objects.get(pk=pk)
    except CategoriaInventario.DoesNotExist:
        return Response({'error': 'Categoría no encontrada'}, status=status.HTTP_404_NOT_FOUND)

    categoria.is_active = False
    categoria.save()
    return Response({'mensaje': 'Categoría eliminada correctamente'}, status=status.HTTP_204_NO_CONTENT)


@swagger_auto_schema(method='get', tags=['Inventario - Categorías'], operation_description="Obtener una categoría por ID")
@api_view(['GET'])
def obtener_categoria(request, pk):
    try:
        categoria = CategoriaInventario.objects.get(pk=pk)
        serializer = CategoriaSerializer(categoria)
        return Response(serializer.data)
    except CategoriaInventario.DoesNotExist:
        return Response({'error': 'Categoría no encontrada'}, status=status.HTTP_404_NOT_FOUND)

@swagger_auto_schema(method='get', tags=['Inventario - Subcategorías'], operation_description="Listar subcategorías activas de una categoría")
@api_view(['GET'])
def listar_subcategorias_por_categoria(request, categoria_id):
    subcategorias = SubcategoriaInventario.objects.filter(categoria_id=categoria_id, is_active=True).order_by('id')
    serializer = SubcategoriaSerializer(subcategorias, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@swagger_auto_schema(method='post', tags=['Inventario - Subcategorías'], operation_description="Crear una subcategoría", request_body=SubcategoriaSerializer)
@api_view(['POST'])
def crear_subcategoria(request):
    serializer = SubcategoriaSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
