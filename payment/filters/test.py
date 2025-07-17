# your_app/filters.py
import django_filters
from general.models import Test

class TestFilter(django_filters.FilterSet):
    material_name = django_filters.NumberFilter(field_name='material_name__id')
    test_name = django_filters.CharFilter(lookup_expr='icontains')
    price_per_piece__gte = django_filters.NumberFilter(field_name='price_per_piece', lookup_expr='gte')
    price_per_piece__lte = django_filters.NumberFilter(field_name='price_per_piece', lookup_expr='lte')
    created_date = django_filters.DateFromToRangeFilter()

    class Meta:
        model = Test
        fields = ['material_name', 'test_name', 'price_per_piece', 'created_date']
