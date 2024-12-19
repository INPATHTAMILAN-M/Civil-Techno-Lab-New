from rest_framework.generics import CreateAPIView, RetrieveAPIView, UpdateAPIView, ListAPIView
from ..models import Quotation
from ..serializers import (
    QuotationCreateSerializer,
    QuotationRetrieveSerializer,
    QuotationListSerializer,
    QuotationUpdateSerializer,
)

# Create API View for Creating Quotations
class QuotationCreateView(CreateAPIView):
    queryset = Quotation.objects.all()
    serializer_class = QuotationCreateSerializer

class QuotationRetrieveView(RetrieveAPIView):
    queryset = Quotation.objects.all()
    serializer_class = QuotationRetrieveSerializer

class QuotationListView(ListAPIView):
    queryset = Quotation.objects.all()
    serializer_class = QuotationListSerializer

class QuotationUpdateView(UpdateAPIView):
    queryset = Quotation.objects.all()
    serializer_class = QuotationUpdateSerializer
