from rest_framework import viewsets
from payment.models import InvoiceTax
from rest_framework.permissions import IsAuthenticated
from payment.pagination import CustomPagination
from payment.serializers import (
    InvoiceTaxRetriveSerializer,
    InvoiceTaxListSerializer,
    InvoiceTaxUpdateSerializer,
    InvoiceTaxCreateSerializer
)


class InvoiceTaxViewSet(viewsets.ModelViewSet):
    queryset = InvoiceTax.objects.all()
    pagination_class = CustomPagination
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'create':
            return InvoiceTaxCreateSerializer
        if self.action in ['update', 'partial_update']:
            return InvoiceTaxUpdateSerializer
        if self.action == 'list':
            return InvoiceTaxListSerializer
        return InvoiceTaxRetriveSerializer
        
