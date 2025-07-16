from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
from payment.pagination import CustomPagination
from django_filters.rest_framework import DjangoFilterBackend
from general.models import Test
from payment.serializers import TestSerializer
from payment.filters import TestFilter

class TestViewSet(viewsets.ModelViewSet):
    queryset = Test.objects.all().order_by('-created_date')
    serializer_class = TestSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_class = TestFilter
    search_fields = ['test_name', 'material_name__material_name']  # adjust based on Material model
