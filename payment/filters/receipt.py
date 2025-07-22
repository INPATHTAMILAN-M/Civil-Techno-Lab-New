import django_filters
from payment.models import Receipt
from django.db.models import Q

class ReceiptFilter(django_filters.FilterSet): 
    search = django_filters.CharFilter(method='filter_by_all')

    def filter_by_all(self, queryset, name, value):
        return queryset.filter(
            Q(receipt_number__icontains=value) |
            Q(customer__customer_name__icontains=value) |
            Q(created_by__username__icontains=value)
        )
    class Meta:
        model = Receipt
        fields = '__all__'  # Adjust fields as necessary