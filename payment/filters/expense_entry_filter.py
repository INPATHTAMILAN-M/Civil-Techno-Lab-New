import django_filters
from payment.models import Expense_Entry
from django.db.models import Q

class ExpenseEntryFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(method='filter_by_all')

    def filter_by_all(self, queryset, name, value):
        return queryset.filter(
            Q(expense_user__icontains=value) 
        )

    from_date = django_filters.DateFilter(
        field_name='created_date', lookup_expr='gte'
    )
    to_date = django_filters.DateFilter(
        field_name='created_date', lookup_expr='lte'
    )
    
    class Meta:
        model = Expense_Entry
        fields = ['search', 'from_date', 'to_date', 'expense_user', 'expense_category']