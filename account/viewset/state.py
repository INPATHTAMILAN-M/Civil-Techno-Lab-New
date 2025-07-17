from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from account.models import State
from account.serializers import StateSerializer

class StateViewSet(viewsets.ModelViewSet):
    queryset = State.objects.all().order_by('name')
    serializer_class = StateSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name']
    ordering_fields = ['name']