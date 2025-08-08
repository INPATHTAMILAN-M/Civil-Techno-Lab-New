from rest_framework import serializers
from payment.models import InvoiceTax
from account.serializers import UserSerializer  # Adjust as needed

# List / Retrieve Serializer
class InvoiceTaxListSerializer(serializers.ModelSerializer):
    invoice_no = serializers.CharField(source='invoice.invoice_no', read_only=True)
    created_by = UserSerializer(read_only=True)
    modified_by = UserSerializer(read_only=True)

    class Meta:
        model = InvoiceTax
        fields = '__all__'

class InvoiceTaxRetriveSerializer(serializers.ModelSerializer):
    invoice_no = serializers.CharField(source='invoice.invoice_no', read_only=True)
    created_by = UserSerializer(read_only=True)
    modified_by = UserSerializer(read_only=True)

    class Meta:
        model = InvoiceTax
        fields = '__all__'

# Create Serializer
class InvoiceTaxCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvoiceTax
        fields = "__all__"


# Update Serializer
class InvoiceTaxUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvoiceTax
        fields = '__all__'
