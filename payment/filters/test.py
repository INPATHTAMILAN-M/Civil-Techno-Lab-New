# your_app/filters.py
import django_filters
from general.models import Test
from django.db.models import Q

class TestFilter(django_filters.FilterSet):
    material_name = django_filters.NumberFilter(field_name='material_name__id')
    test_name = django_filters.CharFilter(lookup_expr='icontains')
    price_per_piece__gte = django_filters.NumberFilter(field_name='price_per_piece', lookup_expr='gte')
    price_per_piece__lte = django_filters.NumberFilter(field_name='price_per_piece', lookup_expr='lte')
    created_date = django_filters.DateFromToRangeFilter()
    search = django_filters.CharFilter(method='filter_by_all')
    from_date = django_filters.DateFilter(field_name='created_date', lookup_expr='gte')
    to_date = django_filters.DateFilter(field_name='created_date', lookup_expr='lte')

    def filter_by_all(self, queryset, name, value):
        return queryset.filter(
            Q(material_name__material_name__icontains=value) |
            Q(test_name__icontains=value)
        )
    class Meta:
        model = Test
        fields = ['material_name', 'test_name', 'price_per_piece', 'created_date']
