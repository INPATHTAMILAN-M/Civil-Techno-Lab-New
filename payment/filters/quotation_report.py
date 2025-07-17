from django_filters import rest_framework as filters
from ..models import QuotationReport
from django.db import models

class QuotationReportFilter(filters.FilterSet):
    start_date = filters.DateFilter(field_name='created_date', lookup_expr='gte')
    end_date = filters.DateFilter(field_name='created_date', lookup_expr='lte')
    created_by = filters.CharFilter(field_name='created_by', lookup_expr='icontains')
    quotation_number = filters.CharFilter(field_name='quotation__quotation_number', lookup_expr='icontains')
    customer = filters.CharFilter(field_name='quotation__customer__id', lookup_expr='exact')

    class Meta:
        model = QuotationReport
        fields = ['start_date', 'end_date', 'created_by', 'quotation', 'customer', 'quotation_number']