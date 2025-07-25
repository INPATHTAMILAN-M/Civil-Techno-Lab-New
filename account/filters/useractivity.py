import django_filters
from django.db.models import Q
from ..models import UserActivity

class UserActivityFilter(django_filters.FilterSet):
    class Meta:
        model = UserActivity
        fields = "__all__"