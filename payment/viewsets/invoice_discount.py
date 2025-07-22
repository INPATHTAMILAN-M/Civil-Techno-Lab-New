# views/invoice_discount_viewset.py

from rest_framework import viewsets
from payment.models import InvoiceDiscount
from payment.serializers import (
    InvoiceDiscountCreateSerializer,
    InvoiceDiscountUpdateSerializer,
    InvoiceDiscountDetailSerializer,
    InvoiceDiscountListSerializer,
)

class InvoiceDiscountViewSet(viewsets.ModelViewSet):
    queryset = InvoiceDiscount.objects.all()

    def get_serializer_class(self):
        if self.action == 'create':
            return InvoiceDiscountCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return InvoiceDiscountUpdateSerializer
        elif self.action == 'retrieve':
            return InvoiceDiscountDetailSerializer
        elif self.action == 'list':
            return InvoiceDiscountListSerializer
        return InvoiceDiscountDetailSerializer

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def perform_update(self, serializer):
        serializer.save(modified_by=self.request.user)
