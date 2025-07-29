from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from account.models import Customer
from payment.pagination import CustomPagination
from account.serializers import (
    CustomerCreateSerializer,
    CustomerListSerializer,
    CustomerRetrieveSerializer,
    CustomerUpdateSerializer
)
from account.filters import CustomerFilter
from rest_framework.permissions import IsAuthenticated

class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all().order_by('-created_date')
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    permission_classes = [IsAuthenticated]
    filterset_class = CustomerFilter
    pagination_class = CustomPagination
    search_fields = ['customer_name', 'phone_no']


    def get_serializer_class(self):
        if self.action == 'create':
            return CustomerCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return CustomerUpdateSerializer
        elif self.action == 'list':
            return CustomerListSerializer
        return CustomerListSerializer
