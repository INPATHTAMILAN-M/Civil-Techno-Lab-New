from rest_framework import serializers
from payment.models import Receipt,Invoice

class invoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invoice
        fields = '__all__'

class ReceiptListSerializer(serializers.ModelSerializer):
    invoice_no = invoiceSerializer(read_only=True)

    class Meta:
        model = Receipt
        fields = '__all__'

class ReceiptCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Receipt
        fields = '__all__'


class ReceiptDetailSerializer(serializers.ModelSerializer):
    invoice_no = invoiceSerializer(read_only=True)

    class Meta:
        model = Receipt
        fields = '__all__'

class ReceiptUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Receipt
        fields = '__all__'


