import django_filters
from payment.models.invoice_models import Invoice

class InvoiceFilter(django_filters.FilterSet):
    class Meta:
        model = Invoice
        fields = "__all__"
        