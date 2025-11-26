from functools import reduce
import operator as op

from django.db.models import Q
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from ..models.proyectoModel import Proyectos
from ..serializers.proyectoSerializer import ProyectoSerializer

