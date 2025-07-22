from django_filters import rest_framework as filters
from django.db import models
from ..models import InvoiceReport
from django.db.models import Q


class InvoiceReportFilter(filters.FilterSet):
    from_date = filters.DateFilter(field_name='created_date', lookup_expr='gte')
    to_date = filters.DateFilter(field_name='created_date', lookup_expr='lte')
    invoice_no = filters.CharFilter(field_name='invoice__invoice_no', lookup_expr='exact')
    project_name = filters.CharFilter(field_name='invoice__project_name', lookup_expr='icontains')
    customer_name = filters.CharFilter(method='filter_customer_name')
    customer = filters.CharFilter(field_name='invoice__customer__id', lookup_expr='exact')
    search = filters.CharFilter(method='filter_by_all')

    def filter_by_all(self, queryset, name, value):
        return queryset.filter(
            Q(invoice__invoice_no__icontains=value) |
            Q(invoice__project_name__icontains=value) |
            Q(invoice__customer__first_name__icontains=value) |
            Q(invoice__customer__last_name__icontains=value)
        )

    def filter_customer_name(self, queryset, name, value):
        return queryset.filter(
            models.Q(customer__first_name__icontains=value) |
            models.Q(customer__last_name__icontains=value)
        )
    class Meta:
        model = InvoiceReport
        fields = ['from_date', 'to_date', 'customer', 'created_by', 'invoice_no', 'project_name', 'customer_name']