from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from general.models import Material
from rest_framework.response import Response
from payment.pagination import CustomPagination
from payment.serializers import MaterialSerializer

class MaterialViewSet(viewsets.ModelViewSet):
    queryset = Material.objects.all().order_by('-created_date')
    serializer_class = MaterialSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    pagination_class = CustomPagination
    search_fields = ['material_name']
    ordering_fields = ['created_date', 'material_name']
    filterset_fields = ['print_format', 'letter_pad_logo', 'created_by']
