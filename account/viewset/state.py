from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from account.models import State
from payment.pagination import CustomPagination

from account.serializers import StateSerializer
from rest_framework.permissions import IsAuthenticated

class StateViewSet(viewsets.ModelViewSet):
    queryset = State.objects.all().order_by('name')
    serializer_class = StateSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    pagination_class = CustomPagination
    search_fields = ['name']
    ordering_fields = ['name']

