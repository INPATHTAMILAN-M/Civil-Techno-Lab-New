from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from general.models import Tax
from general.serializers import TaxSerializer
from payment.pagination import CustomPagination


class TaxViewSet(viewsets.ModelViewSet):
    queryset = Tax.objects.all().order_by('-created_date')
    serializer_class = TaxSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    pagination_class = CustomPagination
    search_fields = ['tax_name']
    ordering_fields = ['tax_name']
    