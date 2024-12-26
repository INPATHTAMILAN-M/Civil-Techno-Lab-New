from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, permissions

from ..models import InvoiceReport
from ..filters import InvoiceReportFilter
from ..serializers import InvoiceReportListSerializer, InvoiceReportDetailSerializer


class InvoiceReportListView(generics.ListAPIView):
    queryset = InvoiceReport.objects.all().order_by('-id')
    serializer_class = InvoiceReportListSerializer    
    filter_backends = [DjangoFilterBackend]
    filterset_class = InvoiceReportFilter
    permission_classes = [permissions.IsAuthenticated]

class InvoiceReportGetView(generics.RetrieveAPIView):
    queryset = InvoiceReport.objects.all().order_by('-id')
    serializer_class = InvoiceReportDetailSerializer 
    permission_classes = [permissions.IsAuthenticated]