from django_filters import rest_framework as filters
from ..models import CustomerDiscount
from django.db.models import Q

class CustomerDiscountFilter(filters.FilterSet):
    search = filters.CharFilter(method='filter_search', label='Search')

    def filter_search(self, queryset, name, value):
        return queryset.filter(
            Q(customer__customer_name__icontains=value) 
        )

    customer = filters.NumberFilter(field_name="customer__id", lookup_expr='exact')
    customer_name = filters.CharFilter(field_name="customer__name", lookup_expr='icontains')
    discount = filters.NumberFilter(field_name="discount__id", lookup_expr='exact')
    created_by = filters.NumberFilter(field_name="created_by__id", lookup_expr='exact')
    created_date = filters.DateFilter(field_name="created_date", lookup_expr='exact')
    created_date__gte = filters.DateFilter(field_name="created_date", lookup_expr='gte')
    created_date__lte = filters.DateFilter(field_name="created_date", lookup_expr='lte')
    modified_by = filters.NumberFilter(field_name="modified_by__id", lookup_expr='exact')
    modified_date = filters.DateTimeFilter(field_name="modified_date", lookup_expr='exact')
    modified_date__gte = filters.DateTimeFilter(field_name="modified_date", lookup_expr='gte')
    modified_date__lte = filters.DateTimeFilter(field_name="modified_date", lookup_expr='lte')

    class Meta:
        model = CustomerDiscount
        fields = '__all__'