from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from api.utils.pagination import CustomPageNumberPagination
from ..models.mantenimientoModel import CentroCosto, Departamento, CuentaContable
from ..serializers.mantenimientoSerializer import (
    CentroCostoSerializer,
    DepartamentoSerializer,
    CuentaContableSerializer,
)


# -------- Centros de Costo --------
search_param = openapi.Parameter('search', openapi.IN_QUERY, description="Filtro por nombre (icontains)", type=openapi.TYPE_STRING)

@swagger_auto_schema(method='get', tags=['Mantenimiento - Centros de Costo'], manual_parameters=[search_param], operation_description="Listar centros de costo activos con paginación y búsqueda")
@api_view(['GET'])
def listar_centros_costo(request):
    qs = CentroCosto.objects.filter(is_active=True)
    q = request.GET.get('search')
    if q:
        qs = qs.filter(nombre__icontains=q)
    qs = qs.order_by('id')
    paginator = CustomPageNumberPagination()
    page = paginator.paginate_queryset(qs, request)
    serializer = CentroCostoSerializer(page, many=True)
    return paginator.get_paginated_response(serializer.data)


@swagger_auto_schema(method='post', tags=['Mantenimiento - Centros de Costo'], operation_description="Crear centro de costo", request_body=CentroCostoSerializer)
@api_view(['POST'])
def crear_centro_costo(request):
    serializer = CentroCostoSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(method='put', tags=['Mantenimiento - Centros de Costo'], operation_description="Actualizar centro de costo", request_body=CentroCostoSerializer)
@api_view(['PUT'])
def actualizar_centro_costo(request, pk):
    try:
        obj = CentroCosto.objects.get(pk=pk)
    except CentroCosto.DoesNotExist:
        return Response({'error': 'Centro de costo no encontrado'}, status=status.HTTP_404_NOT_FOUND)

    serializer = CentroCostoSerializer(obj, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(method='delete', tags=['Mantenimiento - Centros de Costo'], operation_description="Eliminar (soft delete) centro de costo")
@api_view(['DELETE'])
def eliminar_centro_costo(request, pk):
    try:
        obj = CentroCosto.objects.get(pk=pk)
    except CentroCosto.DoesNotExist:
        return Response({'error': 'Centro de costo no encontrado'}, status=status.HTTP_404_NOT_FOUND)

    obj.is_active = False
    obj.save()
    return Response({'mensaje': 'Eliminado correctamente'}, status=status.HTTP_204_NO_CONTENT)


@swagger_auto_schema(method='get', tags=['Mantenimiento - Centros de Costo'], operation_description="Obtener centro de costo por ID")
@api_view(['GET'])
def obtener_centro_costo(request, pk):
    try:
        obj = CentroCosto.objects.get(pk=pk)
    except CentroCosto.DoesNotExist:
        return Response({'error': 'Centro de costo no encontrado'}, status=status.HTTP_404_NOT_FOUND)
    serializer = CentroCostoSerializer(obj)
    return Response(serializer.data)


# -------- Departamentos --------
@swagger_auto_schema(method='get', tags=['Mantenimiento - Departamentos'], manual_parameters=[search_param], operation_description="Listar departamentos activos con paginación y búsqueda")
@api_view(['GET'])
def listar_departamentos(request):
    qs = Departamento.objects.filter(is_active=True)
    q = request.GET.get('search')
    if q:
        qs = qs.filter(nombre__icontains=q)
    qs = qs.order_by('id')
    paginator = CustomPageNumberPagination()
    page = paginator.paginate_queryset(qs, request)
    serializer = DepartamentoSerializer(page, many=True)
    return paginator.get_paginated_response(serializer.data)


@swagger_auto_schema(method='post', tags=['Mantenimiento - Departamentos'], operation_description="Crear departamento", request_body=DepartamentoSerializer)
@api_view(['POST'])
def crear_departamento(request):
    serializer = DepartamentoSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(method='put', tags=['Mantenimiento - Departamentos'], operation_description="Actualizar departamento", request_body=DepartamentoSerializer)
@api_view(['PUT'])
def actualizar_departamento(request, pk):
    try:
        obj = Departamento.objects.get(pk=pk)
    except Departamento.DoesNotExist:
        return Response({'error': 'Departamento no encontrado'}, status=status.HTTP_404_NOT_FOUND)

    serializer = DepartamentoSerializer(obj, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(method='delete', tags=['Mantenimiento - Departamentos'], operation_description="Eliminar (soft delete) departamento")
@api_view(['DELETE'])
def eliminar_departamento(request, pk):
    try:
        obj = Departamento.objects.get(pk=pk)
    except Departamento.DoesNotExist:
        return Response({'error': 'Departamento no encontrado'}, status=status.HTTP_404_NOT_FOUND)

    obj.is_active = False
    obj.save()
    return Response({'mensaje': 'Eliminado correctamente'}, status=status.HTTP_204_NO_CONTENT)


@swagger_auto_schema(method='get', tags=['Mantenimiento - Departamentos'], operation_description="Obtener departamento por ID")
@api_view(['GET'])
def obtener_departamento(request, pk):
    try:
        obj = Departamento.objects.get(pk=pk)
    except Departamento.DoesNotExist:
        return Response({'error': 'Departamento no encontrado'}, status=status.HTTP_404_NOT_FOUND)
    serializer = DepartamentoSerializer(obj)
    return Response(serializer.data)


# -------- Cuentas Contables --------
@swagger_auto_schema(method='get', tags=['Mantenimiento - Cuentas Contables'], manual_parameters=[search_param], operation_description="Listar cuentas contables activas con paginación y búsqueda")
@api_view(['GET'])
def listar_cuentas_contables(request):
    qs = CuentaContable.objects.filter(is_active=True)
    q = request.GET.get('search')
    if q:
        qs = qs.filter(nombre__icontains=q)
    qs = qs.order_by('id')
    paginator = CustomPageNumberPagination()
    page = paginator.paginate_queryset(qs, request)
    serializer = CuentaContableSerializer(page, many=True)
    return paginator.get_paginated_response(serializer.data)


@swagger_auto_schema(method='post', tags=['Mantenimiento - Cuentas Contables'], operation_description="Crear cuenta contable", request_body=CuentaContableSerializer)
@api_view(['POST'])
def crear_cuenta_contable(request):
    serializer = CuentaContableSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(method='put', tags=['Mantenimiento - Cuentas Contables'], operation_description="Actualizar cuenta contable", request_body=CuentaContableSerializer)
@api_view(['PUT'])
def actualizar_cuenta_contable(request, pk):
    try:
        obj = CuentaContable.objects.get(pk=pk)
    except CuentaContable.DoesNotExist:
        return Response({'error': 'Cuenta contable no encontrada'}, status=status.HTTP_404_NOT_FOUND)

    serializer = CuentaContableSerializer(obj, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(method='delete', tags=['Mantenimiento - Cuentas Contables'], operation_description="Eliminar (soft delete) cuenta contable")
@api_view(['DELETE'])
def eliminar_cuenta_contable(request, pk):
    try:
        obj = CuentaContable.objects.get(pk=pk)
    except CuentaContable.DoesNotExist:
        return Response({'error': 'Cuenta contable no encontrada'}, status=status.HTTP_404_NOT_FOUND)

    obj.is_active = False
    obj.save()
    return Response({'mensaje': 'Eliminado correctamente'}, status=status.HTTP_204_NO_CONTENT)


@swagger_auto_schema(method='get', tags=['Mantenimiento - Cuentas Contables'], operation_description="Obtener cuenta contable por ID")
@api_view(['GET'])
def obtener_cuenta_contable(request, pk):
    try:
        obj = CuentaContable.objects.get(pk=pk)
    except CuentaContable.DoesNotExist:
        return Response({'error': 'Cuenta contable no encontrada'}, status=status.HTTP_404_NOT_FOUND)
    serializer = CuentaContableSerializer(obj)
    return Response(serializer.data)
