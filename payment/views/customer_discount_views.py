from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from ..models import CustomerDiscount
from ..filters.customer_discount_filter import CustomerDiscountFilter
from ..serializers import (
    CustomerDiscountCreateSerializer,
    CustomerDiscountUpdateSerializer,
    CustomerDiscountRetrieveSerializer,
    CustomerDiscountListSerializer,
)

class CustomerDiscountPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class CustomerDiscountViewSet(viewsets.ModelViewSet):
    queryset = CustomerDiscount.objects.all().order_by('-id')
    filterset_class = CustomerDiscountFilter
    permission_classes = [IsAuthenticated]
    pagination_class = CustomerDiscountPagination
    filter_backends = [DjangoFilterBackend]
    http_method_names = ['get', 'post', 'patch', 'delete']


    def get_serializer_class(self):
        if self.action == 'create':
            return CustomerDiscountCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return CustomerDiscountUpdateSerializer
        elif self.action == 'retrieve':
            return CustomerDiscountRetrieveSerializer
        elif self.action == 'list':
            return CustomerDiscountListSerializer
        return super().get_serializer_class()

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def perform_update(self, serializer):
        serializer.save(modified_by=self.request.user)
