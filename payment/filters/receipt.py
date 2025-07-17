import django_filters
from payment.models import Receipt

class ReceiptFilter(django_filters.FilterSet):
    class Meta:
        model = Receipt
        fields = '__all__'  # Adjust fields as necessary