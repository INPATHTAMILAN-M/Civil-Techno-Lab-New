from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from payment.pagination import CustomPagination
from ..filters.material_filter import MaterialFilter

from ..models import Material, Print_Format, Letter_Pad_Logo
from ..serializers.material_serializer import (
    Create_Material_Serializer,
    Material_Serializer,

)

class MaterialViewSet(viewsets.ModelViewSet):
    queryset = Material.objects.all().order_by('-created_date')
    serializer_class = Material_Serializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    pagination_class = CustomPagination
    filterset_class = MaterialFilter
