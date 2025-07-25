# auditlog_api/viewsets.py

from rest_framework import viewsets, filters
from auditlog.models import LogEntry
from account.serializers import LogEntrySerializer
from rest_framework.permissions import IsAuthenticated
from payment.pagination import CustomPagination  # Assuming you have a custom pagination class

class LogEntryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = LogEntry.objects.all().select_related('actor', 'content_type')
    serializer_class = LogEntrySerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination  # Disable pagination if not needed
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['actor__username', 'object_repr', 'changes']
    ordering_fields = ['timestamp']
    ordering = ['-timestamp']
