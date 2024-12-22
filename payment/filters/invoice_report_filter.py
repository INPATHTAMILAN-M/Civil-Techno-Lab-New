from django_filters import rest_framework as filters
from ..models import InvoiceReport


class InvoiceReportFilter(filters.FilterSet):
    start_date = filters.DateFilter(field_name='created_date', lookup_expr='gte')
    end_date = filters.DateFilter(field_name='created_date', lookup_expr='lte')
    created_by = filters.CharFilter(field_name='created_by__username', lookup_expr='icontains')
    quotation = filters.CharFilter(field_name='quotation__quotation_number', lookup_expr='icontains')
    
    class Meta:
        model = InvoiceReport
        fields = ['start_date', 'end_date', 'created_by', 'invoice']