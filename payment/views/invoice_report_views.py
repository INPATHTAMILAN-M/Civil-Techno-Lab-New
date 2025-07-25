import io
import zipfile
from django.http import FileResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from payment.pagination import CustomPagination

from ..models import InvoiceReport
from ..filters import InvoiceReportFilter
from ..serializers import InvoiceReportListSerializer, InvoiceReportDetailSerializer


class InvoiceReportListView(generics.ListAPIView):
    queryset = InvoiceReport.objects.all().order_by('-invoice__id')
    serializer_class = InvoiceReportListSerializer    
    filter_backends = [DjangoFilterBackend]
    filterset_class = InvoiceReportFilter    
    pagination_class = CustomPagination
    permission_classes = [permissions.IsAuthenticated]

class InvoiceReportGetView(generics.RetrieveAPIView):
    queryset = InvoiceReport.objects.all().order_by('-id')
    serializer_class = InvoiceReportDetailSerializer 
    permission_classes = [permissions.IsAuthenticated]



class InvoiceReportZipAPIView(APIView):
    def get(self, request, *args, **kwargs):
        # Get month and year from query parameters
        month = request.query_params.get('month')
        year = request.query_params.get('year')

        if not month or not year:
            return Response(
                {"error": "Month and year parameters are required."},
                status=status.HTTP_400_BAD_REQUEST
            )
        from django.utils import timezone
        from datetime import timedelta
        today = timezone.now().date()
        seven_days_ago = today - timedelta(days=7)

        # # Filter InvoiceReports based on the month and year
        # filtered_reports = InvoiceReport.objects.filter(
        #     invoice__created_date__year=year,
        #     invoice__created_date__month=month
        # )
        filtered_reports = InvoiceReport.objects.filter(
        invoice__created_date__date__gte=seven_days_ago,
        invoice__created_date__date__lte=today
    )

        if not filtered_reports.exists():
            return Response(
                {"error": "No reports found for the given month and year."},
                status=status.HTTP_404_NOT_FOUND
            )

        # Create an in-memory ZIP file
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, "w") as zip_file:
            for report in filtered_reports:
                if report.invoice_file:  # Ensure file exists
                    with report.invoice_file.open('rb') as file:
                        safe_invoice_no = str(report.invoice.invoice_no).replace("/", "_")
                        zip_file.writestr(f"invoice__{safe_invoice_no}.pdf", file.read())

        zip_buffer.seek(0)

        # Create and return the ZIP file response
        response = FileResponse(zip_buffer, as_attachment=True, filename="invoice_reports.zip")
        return response