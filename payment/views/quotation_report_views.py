from rest_framework import generics, permissions
from rest_framework.parsers import MultiPartParser, FormParser
from django_filters.rest_framework import DjangoFilterBackend

from payment.pagination import CustomPagination

from ..models import QuotationReport
from ..filters import QuotationReportFilter
from ..serializers import (
    QuotationReportListSerializer,
    QuotationReportDetailSerializer,
    QuotationReportCreateSerializer,
    QuotationReportUpdateSerializer
)


class QuotationReportList(generics.ListAPIView):
    queryset = QuotationReport.objects.all().order_by('-id')
    serializer_class = QuotationReportListSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = QuotationReportFilter
    pagination_class = CustomPagination
    permission_classes = [permissions.IsAuthenticated]

class QuotationReportCreate(generics.CreateAPIView):
    queryset = QuotationReport.objects.all()
    serializer_class = QuotationReportCreateSerializer
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

class QuotationReportDetail(generics.RetrieveAPIView):
    queryset = QuotationReport.objects.all().order_by('-id')
    serializer_class = QuotationReportDetailSerializer
    permission_classes = [permissions.IsAuthenticated]

class QuotationReportUpdate(generics.UpdateAPIView):
    queryset = QuotationReport.objects.all()
    serializer_class = QuotationReportUpdateSerializer
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ['patch']    