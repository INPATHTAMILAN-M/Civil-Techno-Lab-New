import django_filters
from payment.models import Invoice_File
from django.db.models import Q

class InvoiceFileFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(method='filter_by_all')

    def filter_by_all(self, queryset, name, value):
        return queryset.filter(
            Q(invoice__invoice_no__icontains=value) |
            Q(expense__icontains=value)
        )
    invoice_no = django_filters.CharFilter(field_name='invoice__invoice_no', lookup_expr='exact')
    from_date = django_filters.DateFilter(
        field_name='created_date', lookup_expr='gte'
    )
    to_date = django_filters.DateFilter(
        field_name='created_date', lookup_expr='lte'
    )
    
    class Meta:
        model = Invoice_File
        fields = ['search', 'from_date', 'to_date', 'invoice_no', 'expense', 'category']
