
import django_filters
from django_filters import rest_framework as filters
from payment.models import QuotationItem
from django.db.models import Q

class QuotationItemFilter(django_filters.FilterSet):
    test = filters.CharFilter(field_name='test__name', lookup_expr='icontains')
    quotation = filters.NumberFilter(field_name='quotation__id')
    created_by = filters.CharFilter(field_name='created_by__username', lookup_expr='icontains')
    modified_by = filters.CharFilter(field_name='modified_by__username', lookup_expr='icontains')
    created_date = filters.DateFromToRangeFilter()
    modified_date = filters.DateTimeFromToRangeFilter()
    price_per_sample = filters.RangeFilter()
    quantity = filters.RangeFilter()
    is_authorised_signatory = filters.BooleanFilter()
    search = filters.CharFilter(method='filter_by_all')

    def filter_by_all(self, queryset, name, value):
        return queryset.filter(
            Q(test__name__icontains=value) |
            Q(quotation__quotation_number__icontains=value) |
            Q(created_by__username__icontains=value) |
            Q(modified_by__username__icontains=value)
        )
    class Meta:
        model = QuotationItem
        fields = [
            'test',
            'quotation',
            'created_by',
            'modified_by',
            'created_date',
            'modified_date',
            'price_per_sample',
            'quantity',
            'is_authorised_signatory',
        ]
