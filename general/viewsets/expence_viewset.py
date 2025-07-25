from rest_framework import viewsets
from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from payment.pagination import CustomPagination
from ..filters.expence_filter import ExpenceFilter
from ..models import Expense
from ..serializers.expence_serializer import (
    Expense_Serializer
)

class ExpenseViewSet(viewsets.ModelViewSet):
    queryset = Expense.objects.all().order_by('-created_date')
    serializer_class = Expense_Serializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    pagination_class = CustomPagination
    filterset_class = ExpenceFilter


    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def perform_update(self, serializer):
        serializer.save(modified_by=self.request.user)
