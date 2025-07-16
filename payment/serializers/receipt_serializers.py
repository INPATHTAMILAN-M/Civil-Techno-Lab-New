from rest_framework import serializers
from payment.models import Receipt,Invoice

class invoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invoice
        fields = '__all__'

class ReceiptSerializer(serializers.ModelSerializer):
    invoice_no = invoiceSerializer(read_only=True)

    class Meta:
        model = Receipt
        fields = '__all__'

