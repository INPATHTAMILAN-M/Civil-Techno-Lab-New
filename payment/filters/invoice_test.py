import django_filters
from payment.models import Invoice_Test

class InvoiceTestFilter(django_filters.FilterSet):
    class Meta:
        model = Invoice_Test
        fields = "__all__"