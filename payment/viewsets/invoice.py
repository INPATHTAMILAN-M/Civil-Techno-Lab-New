from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from payment.pagination import CustomPagination
from payment.models import Invoice
from payment.serializers import InvoiceSerializer
from payment.filters import InvoiceFilter


class InvoiceViewSet(viewsets.ModelViewSet):
    queryset = Invoice.objects.all().order_by('-created_date')
    serializer_class = InvoiceSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    pagination_class = CustomPagination
    permission_classes = [IsAuthenticated]
    filterset_class = InvoiceFilter
    search_fields = ['invoice_no', 'project_name', 'customer__customer_name']

    
