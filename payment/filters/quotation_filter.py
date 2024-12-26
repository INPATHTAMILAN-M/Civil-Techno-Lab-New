
import django_filters
from django_filters import DateFilter, CharFilter
from django.db import models

from ..models import Quotation


class QuotationFilter(django_filters.FilterSet):
    start_date = DateFilter(field_name='date_created', lookup_expr='gte')
    end_date = DateFilter(field_name='date_created', lookup_expr='lte')
    quotation_number = CharFilter(field_name='quotation_number', lookup_expr='icontains')
    customer_name = CharFilter(method='filter_customer_name')
    customer = CharFilter(field_name='customer', lookup_expr='exact')

    def filter_customer_name(self, queryset, name, value):
        return queryset.filter(
            models.Q(customer__first_name__icontains=value) |
            models.Q(customer__last_name__icontains=value)
        )

    class Meta:
        model = Quotation
        fields = ['quotation_number', 'customer', 'customer_name','completed', 'created_by']
