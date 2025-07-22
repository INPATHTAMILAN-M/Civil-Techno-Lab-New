from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from ..models import Invoice_File
from payment.pagination import CustomPagination
from payment.filters.invoice_file_filter import InvoiceFileFilter
from ..serializers import Invoice_File_Serializer


class InvoiceFileViewSet(viewsets.ModelViewSet):
    queryset = Invoice_File.objects.all().order_by('-created_date')
    serializer_class = Invoice_File_Serializer
    filter_backends = [DjangoFilterBackend,]
    pagination_class = CustomPagination
    filterset_class = InvoiceFileFilter

