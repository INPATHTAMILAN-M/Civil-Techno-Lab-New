from django_filters import rest_framework as filters
from django.db.models import Q
from general.models import Material

class MaterialFilter(filters.FilterSet):
    search = filters.CharFilter(method='filter_by_all')

    class Meta:
        model = Material
        fields = []

    def filter_by_all(self, queryset, name, value):
        return queryset.filter(
            Q(material_name__icontains=value)
        )
