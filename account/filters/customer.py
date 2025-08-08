from django_filters import rest_framework as filters
from account.models import Customer
from django.db.models import Q

class CustomerFilter(filters.FilterSet):
    search = filters.CharFilter(method='filter_by_all')

    class Meta:
        model = Customer
        fields = '__all__'

    def filter_by_all(self, queryset, name, value):
        return queryset.filter(
            Q(email__icontains=value) |
            Q(customer_name__icontains=value) |
            Q(phone_no__icontains=value) 
        )