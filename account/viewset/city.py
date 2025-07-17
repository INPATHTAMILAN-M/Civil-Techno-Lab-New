from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from account.models import City
from account.serializers import CitySerializer



class CityViewSet(viewsets.ModelViewSet):
    queryset = City.objects.all().order_by('-created_date')
    serializer_class = CitySerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name']
    ordering_fields = ['created_date', 'name']
    filterset_fields = ['created_by', 'modified_by']
