import django_filters
from payment.models import Receipt

class ReceiptFilter(django_filters.FilterSet):
    invoice_no = django_filters.NumberFilter(field_name='invoice_no__id')
    payment_mode = django_filters.CharFilter(lookup_expr='iexact')
    date = django_filters.DateFromToRangeFilter()  # ?date_after=YYYY-MM-DD&date_before=YYYY-MM-DD
    amount__gte = django_filters.NumberFilter(field_name='amount', lookup_expr='gte')
    amount__lte = django_filters.NumberFilter(field_name='amount', lookup_expr='lte')
    created_by = django_filters.NumberFilter(field_name='created_by__id')

    class Meta:
        model = Receipt
        fields = ['invoice_no', 'payment_mode', 'date', 'amount', 'created_by']