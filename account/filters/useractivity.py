import django_filters
from django.db.models import Q
from ..models import UserActivity

class UserActivityFilter(django_filters.FilterSet):
    login_at = django_filters.DateFromToRangeFilter(field_name='login_at')
    class Meta:
        model = UserActivity
        fields = "__all__"