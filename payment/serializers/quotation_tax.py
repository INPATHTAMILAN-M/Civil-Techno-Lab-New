from rest_framework import serializers
from payment.models import QuotationTax


class QuotationTaxSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuotationTax
        fields = '__all__'