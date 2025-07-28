from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication, BaseAuthentication
from payment.models.invoice_models import Expense_Entry
from ..models import Quotation

from payment.pagination import CustomPagination
from ..serializers import Expense_Entry_Serializer
from ..filters.expense_entry_filter import ExpenseEntryFilter

class Expense_Entry_ViewSet(viewsets.ModelViewSet):
    queryset = Expense_Entry.objects.all().order_by('-created_date')
    serializer_class = Expense_Entry_Serializer
    filter_backends = [DjangoFilterBackend,]
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination
    filterset_class = ExpenseEntryFilter