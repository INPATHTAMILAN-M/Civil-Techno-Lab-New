from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics

from ..models import InvoiceReport
from ..filters import InvoiceReportFilter
from ..serializers import InvoiceReportListSerializer, InvoiceReportDetailSerializer


class InvoiceReportListView(generics.ListAPIView):
    queryset = InvoiceReport.objects.all()
    serializer_class = InvoiceReportListSerializer    
    filter_backends = [DjangoFilterBackend]
    filterset_class = InvoiceReportFilter

class InvoiceReportGetView(generics.RetrieveAPIView):
    queryset = InvoiceReport.objects.all()
    serializer_class = InvoiceReportDetailSerializer 