from django_filters import rest_framework as filters
from django.db.models import Q
from general.models import Expense

class ExpenceFilter(filters.FilterSet):
    search = filters.CharFilter(method='filter_by_all')

    class Meta:
        model = Expense
        fields = []

    def filter_by_all(self, queryset, name, value):
        return queryset.filter(
            Q(expense_name__icontains=value)
        )
