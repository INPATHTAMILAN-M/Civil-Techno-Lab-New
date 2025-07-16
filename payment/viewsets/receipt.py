from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
from payment.pagination import CustomPagination
from django_filters.rest_framework import DjangoFilterBackend
from payment.models import Receipt
from payment.serializers import ReceiptSerializer
from payment.filters import ReceiptFilter


class ReceiptViewSet(viewsets.ModelViewSet):
    queryset = Receipt.objects.all().order_by('-created_date')
    serializer_class = ReceiptSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination
    filterset_class = ReceiptFilter
    search_fields = ['cheque_number', 'upi', 'neft', 'tds', 'payment_mode', 
                     'invoice_no__invoice_no']
