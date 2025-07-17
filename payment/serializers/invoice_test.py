from rest_framework import serializers
from payment.models import Invoice_Test
from general.models import Test

class TestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Test
        fields = '__all__'

class InvoiceTestListSerializer(serializers.ModelSerializer):
    test = TestSerializer(read_only=True)

    class Meta:
        model = Invoice_Test
        fields = '__all__'

class InvoiceTestDetailSerializer(serializers.ModelSerializer):
    test = TestSerializer(read_only=True)

    class Meta:
        model = Invoice_Test
        fields = '__all__'

class InvoiceTestCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invoice_Test
        fields = ['quantity', 'total', 'price_per_sample', 'invoice', 'test']

class InvoiceTestUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invoice_Test
        fields = '__all__'
        read_only_fields = ['created_by', 'invoice_image', 'report_template']
