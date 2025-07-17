from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from account.models import Country
from account.serializers import CountrySerializer




class CountryViewSet(viewsets.ModelViewSet):
    queryset = Country.objects.all().order_by('name')
    serializer_class = CountrySerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name']
    ordering_fields = ['name']