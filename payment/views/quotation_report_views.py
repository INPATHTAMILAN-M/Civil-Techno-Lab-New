from rest_framework import generics, permissions
from rest_framework.parsers import MultiPartParser, FormParser
from ..models import QuotationReport
from ..serializers import (
    QuotationReportListSerializer,
    QuotationReportDetailSerializer,
    QuotationReportCreateSerializer,
    QuotationReportUpdateSerializer
)

class QuotationReportList(generics.ListAPIView):
    queryset = QuotationReport.objects.all()
    serializer_class = QuotationReportListSerializer
    permission_classes = [permissions.IsAuthenticated]

class QuotationReportCreate(generics.CreateAPIView):
    queryset = QuotationReport.objects.all()
    serializer_class = QuotationReportCreateSerializer
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

class QuotationReportDetail(generics.RetrieveDestroyAPIView):
    queryset = QuotationReport.objects.all()
    serializer_class = QuotationReportDetailSerializer
    permission_classes = [permissions.IsAuthenticated]

class QuotationReportUpdate(generics.UpdateAPIView):
    queryset = QuotationReport.objects.all()
    serializer_class = QuotationReportUpdateSerializer
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = [permissions.IsAuthenticated]