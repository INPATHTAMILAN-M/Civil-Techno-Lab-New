from rest_framework import viewsets
from payment.models import InvoiceTax, QuotationTax
from payment.serializers import QuotationTaxSerializer
from rest_framework.permissions import IsAuthenticated
from payment.pagination import CustomPagination

class QuotationTaxViewSet(viewsets.ModelViewSet):
    queryset = QuotationTax.objects.all()
    serializer_class = QuotationTaxSerializer
    pagination_class = CustomPagination
    permission_classes = [IsAuthenticated]
