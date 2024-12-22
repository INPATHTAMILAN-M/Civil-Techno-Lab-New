from payment.models import InvoiceReport
from ..serializers import InvoiceReportListSerializer, InvoiceReportDetailSerializer
from rest_framework import generics

class InvoiceReportListView(generics.ListAPIView):
    queryset = InvoiceReport.objects.all()
    serializer_class = InvoiceReportListSerializer    
    # permission_classes = [IsAuthenticated]

class InvoiceReportGetView(generics.RetrieveAPIView):
    queryset = InvoiceReport.objects.all()
    serializer_class = InvoiceReportDetailSerializer 