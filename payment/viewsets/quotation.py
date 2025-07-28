from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from ..models import Quotation
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication,BasicAuthentication
from payment.pagination import CustomPagination
from ..serializers.quotation import QuotationListSerializer
from ..filters.quotation import QuotationFilter

class QuotationViewSet(viewsets.ModelViewSet):
    queryset = Quotation.objects.all().order_by('-created_date')
    serializer_class = QuotationListSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    pagination_class = CustomPagination
    permission_classes = [IsAuthenticated]
    filterset_fields = ['print_format', 'letter_pad_logo', 'created_by']
    filterset_class = QuotationFilter