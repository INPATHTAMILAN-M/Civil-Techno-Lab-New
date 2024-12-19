from rest_framework.generics import CreateAPIView, RetrieveAPIView, UpdateAPIView, ListAPIView
from payment.models import QuotationItem
from ..serializers import (
    QuotationItemCreateSerializer,
    QuotationItemListSerializer,
    QuotationItemGetSerializer,
    QuotationItemUpdateSerializer,
)

# Create API View for Creating Quotation Items
class QuotationItemCreateView(CreateAPIView):
    queryset = QuotationItem.objects.all()
    serializer_class = QuotationItemCreateSerializer


# List API View for Listing All Quotation Items
class QuotationItemListView(ListAPIView):
    queryset = QuotationItem.objects.all()
    serializer_class = QuotationItemListSerializer


# Retrieve API View for Getting a Single Quotation Item
class QuotationItemRetrieveView(RetrieveAPIView):
    queryset = QuotationItem.objects.all()
    serializer_class = QuotationItemGetSerializer


# Update API View for Updating a Quotation Item
class QuotationItemUpdateView(UpdateAPIView):
    queryset = QuotationItem.objects.all()
    serializer_class = QuotationItemUpdateSerializer
