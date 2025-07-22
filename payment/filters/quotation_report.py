from django_filters import rest_framework as filters
from ..models import QuotationReport
from django.db import models
from django.db.models import Q

class QuotationReportFilter(filters.FilterSet):
    from_date = filters.DateFilter(field_name='created_date', lookup_expr='gte')
    to_date = filters.DateFilter(field_name='created_date', lookup_expr='lte')
    created_by = filters.CharFilter(field_name='created_by', lookup_expr='icontains')
    quotation_number = filters.CharFilter(field_name='quotation__quotation_number', lookup_expr='icontains')
    customer = filters.CharFilter(field_name='quotation__customer__id', lookup_expr='exact')
    search = filters.CharFilter(method='filter_by_all')

    def filter_by_all(self, queryset, name, value):
        return queryset.filter(
            Q(quotation__quotation_number__icontains=value) |
            Q(quotation__customer__first_name__icontains=value) |
            Q(quotation__customer__last_name__icontains=value)
        )
    class Meta:
        model = QuotationReport
        fields = ['from_date', 'to_date', 'created_by', 'quotation', 'customer', 'quotation_number']