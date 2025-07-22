# serializers/invoice_discount_serializers.py

from rest_framework import serializers
from payment.models import InvoiceDiscount
from payment.serializers import InvoiceListSerializer  # Adjust import
from django.contrib.auth import get_user_model

User = get_user_model()

class InvoiceDiscountBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvoiceDiscount
        fields = '__all__'

class InvoiceDiscountCreateSerializer(serializers.ModelSerializer):
    discount = serializers.FloatField(required=True, min_value=0, max_value=100)
    class Meta:
        model = InvoiceDiscount
        fields = '__all__'

    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user
        return super().create(validated_data)

class InvoiceDiscountUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvoiceDiscount
        fields = ['discount']

    def update(self, instance, validated_data):
        instance.modified_by = self.context['request'].user
        return super().update(instance, validated_data)

class InvoiceDiscountDetailSerializer(serializers.ModelSerializer):
    invoice = InvoiceListSerializer(read_only=True)
    created_by = serializers.StringRelatedField()
    modified_by = serializers.StringRelatedField()

    class Meta:
        model = InvoiceDiscount
        fields = '__all__'

class InvoiceDiscountListSerializer(serializers.ModelSerializer):
    invoice = serializers.StringRelatedField()

    class Meta:
        model = InvoiceDiscount
        fields = ['id', 'invoice', 'discount', 'created_date', 'modified_date']
