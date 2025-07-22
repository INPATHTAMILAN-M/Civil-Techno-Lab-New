import django_filters
from payment.models import Invoice_Test
from django.db.models import Q

class InvoiceTestFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(method='filter_by_all')

    def filter_by_all(self, queryset, name, value):
        return queryset.filter(
            Q(invoice_number__icontains=value) |
            Q(customer__customer_name__icontains=value) |
            Q(created_by__username__icontains=value)
        )
    from_date = django_filters.DateFilter(
        field_name='created_date', lookup_expr='gte'
    )
    to_date = django_filters.DateFilter(
        field_name='created_date', lookup_expr='lte'
    )
    class Meta:
        model = Invoice_Test
        fields = "__all__"