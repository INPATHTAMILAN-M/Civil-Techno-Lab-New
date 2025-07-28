from rest_framework import viewsets, filters
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication,BasicAuthentication
from django_filters.rest_framework import DjangoFilterBackend
from payment.pagination import CustomPagination
from payment.models import Invoice
from payment.serializers import (
    InvoiceCreateSerializer,
    InvoiceUpdateSerializer,
    InvoiceListSerializer,
    InvoiceRetrieveSerializer,

)
from payment.filters import InvoiceFilter
from general.models import Tax


class InvoiceViewSet(viewsets.ModelViewSet):
    queryset = Invoice.objects.all().order_by('-created_date')
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    pagination_class = CustomPagination
    permission_classes = [IsAuthenticated]
    filterset_class = InvoiceFilter
    search_fields = ['invoice_no', 'project_name', 'customer__customer_name']

    def get_serializer_class(self):
        if self.action == 'create':
            return InvoiceCreateSerializer
        if self.action in ['update', 'partial_update']:
            return InvoiceUpdateSerializer
        if self.action == 'list':
            return InvoiceListSerializer
        return InvoiceRetrieveSerializer
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True) 
        first_two_taxes = Tax.objects.all()[:2]
        instance = serializer.save(created_by=request.user)
        instance.tax.set(first_two_taxes)
        instance.save()
        serializer = InvoiceRetrieveSerializer(instance)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    
