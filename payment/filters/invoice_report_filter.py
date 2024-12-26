from django_filters import rest_framework as filters
from django.db import models
from ..models import InvoiceReport


class InvoiceReportFilter(filters.FilterSet):
    start_date = filters.DateFilter(field_name='created_date', lookup_expr='gte')
    end_date = filters.DateFilter(field_name='created_date', lookup_expr='lte')
    invoice_number = filters.CharFilter(field_name='invoice__invoice_no', lookup_expr='icontains')
    project_name = filters.CharFilter(field_name='invoice__project_name', lookup_expr='icontains')
    customer_name = filters.CharFilter(method='filter_customer_name')
    customer = filters.CharFilter(field_name='invoice__customer__id', lookup_expr='exact')
    

    def filter_customer_name(self, queryset, name, value):
        return queryset.filter(
            models.Q(customer__first_name__icontains=value) |
            models.Q(customer__last_name__icontains=value)
        )
    class Meta:
        model = InvoiceReport
        fields = ['start_date', 'end_date', 'customer', 'created_by', 'invoice_number', 'project_name', 'customer_name']