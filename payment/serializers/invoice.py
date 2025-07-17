from rest_framework import serializers
from payment.models import Invoice, SalesMode
from general.models import Tax
from account.models import Customer


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = "__all__"

class SalesModeSerializer(serializers.ModelSerializer):
    class Meta:
        model = SalesMode
        fields = "__all__"

class TaxSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tax
        fields = "__all__"


class InvoiceSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer(read_only=True)
    sales_mode = SalesModeSerializer(read_only=True)
    tax = TaxSerializer(many=True, read_only=True)
    
    customer_id = serializers.PrimaryKeyRelatedField(queryset=Customer.objects.all(), write_only=True, source='customer')
    sales_mode_id = serializers.PrimaryKeyRelatedField(queryset=SalesMode.objects.all(), write_only=True, source='sales_mode')
    tax_ids = serializers.PrimaryKeyRelatedField(queryset=Tax.objects.all(), many=True, write_only=True, source='tax')

    class Meta:
        model = Invoice
        fields = [
            'id', 'invoice_no', 'project_name', 'date',
            'discount', 'advance', 'balance', 'total_amount', 'tds_amount',
            'fully_paid', 'payment_mode', 'cheque_number', 'upi', 'bank',
            'amount_paid_date', 'invoice_image', 'place_of_testing', 'completed',
            'is_old_invoice_format', 'created_date', 'modified_date',
            'customer', 'sales_mode', 'tax',
            'customer_id', 'sales_mode_id', 'tax_ids'
        ]
