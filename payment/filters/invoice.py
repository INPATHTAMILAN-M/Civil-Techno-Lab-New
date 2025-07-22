import django_filters
from payment.models.invoice_models import Invoice
from django.db.models import Q

class InvoiceFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(method='filter_by_all')
    
    from_date = django_filters.DateFilter(
        field_name='created_date', 
        lookup_expr='gte'
    )
    
    to_date = django_filters.DateFilter(
        field_name='created_date', 
        lookup_expr='lte'
    )
    invoice_no = django_filters.CharFilter(
        field_name='invoice_no', 
        lookup_expr='exact'
    )
    
    def filter_by_all(self, queryset, name, value):
        return queryset.filter(
            Q(invoice_no__icontains=value) |
            Q(project_name__icontains=value) |
            Q(customer__customer_name__icontains=value) |
            Q(completed__icontains=value)
        )
        
    class Meta:
        model = Invoice
        fields = ['search', 'customer', 'from_date', 'to_date', 'completed', 'invoice_no', 'project_name','fully_paid']
