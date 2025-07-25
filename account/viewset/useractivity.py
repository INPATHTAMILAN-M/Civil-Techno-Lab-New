from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework import filters
from account.models import UserActivity
from account.serializers import UserLogGetSerializer
from payment.pagination import CustomPagination
from django_filters.rest_framework import DjangoFilterBackend
from account.filters import UserActivityFilter

class UserlogsViewSet(ReadOnlyModelViewSet):
    """
    A read-only viewset for viewing user activity logs.
    Accepts only GET (list and retrieve).
    """
    queryset = UserActivity.objects.all().order_by('-id')
    serializer_class = UserLogGetSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = UserActivityFilter
    search_fields = ['user__username', 'action', 'details']
    pagination_class = CustomPagination
    
