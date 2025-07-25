from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from ..models import Invoice_File
from payment.pagination import CustomPagination
from payment.filters.invoice_file_filter import InvoiceFileFilter
from rest_framework.authentication import TokenAuthentication, BaseAuthentication
from payment.serializers import (
    InvoiceFileListSerializer,
    InvoiceFileRetrieveSerializer,
    InvoiceFileUpdateSerializer,
    InvoiceFileCreateSerializer

)


class InvoiceFileViewSet(viewsets.ModelViewSet):
    queryset = Invoice_File.objects.all().order_by('-created_date')
    filter_backends = [DjangoFilterBackend,]
    # authentication_classes = [TokenAuthentication,BaseAuthentication]
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination
    filterset_class = InvoiceFileFilter
    


    def get_serializer_class(self):
        if self.action == 'create':
            return InvoiceFileCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return InvoiceFileUpdateSerializer
        elif self.action == 'retrieve':
            return InvoiceFileRetrieveSerializer
        elif self.action == 'list':
            return InvoiceFileListSerializer
        return InvoiceFileRetrieveSerializer
