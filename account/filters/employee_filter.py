import django_filters
from django.db.models import Q
from ..models import Employee

class EmployeeFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(method='filter_by_all')

    class Meta:
        model = Employee
        fields = []

    def filter_by_all(self, queryset, name, value):
        return queryset.filter(
            Q(employee_name__icontains=value) |
            Q(mobile_number__icontains=value) |
            Q(user__username__icontains=value)
        )
