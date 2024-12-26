from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import CreateAPIView, RetrieveAPIView, UpdateAPIView, ListAPIView

from general.models import Tax
from general.serializers.tax_serializer import TaxListSerializer
# from ..serializers.tax_serializer import TaxListSerializer

class TaxListView(ListAPIView):
    queryset = Tax.objects.all()
    serializer_class = TaxListSerializer
    filter_backends = [DjangoFilterBackend]

class TaxEnableListView(ListAPIView):
    queryset = Tax.objects.filter(tax_status='E')
    serializer_class = TaxListSerializer
    filter_backends = [DjangoFilterBackend]