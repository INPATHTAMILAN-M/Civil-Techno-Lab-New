from rest_framework import serializers
from ..models import CustomerDiscount
from account.models import Customer



class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['id','customer_name','email']

class CustomerDiscountCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerDiscount
        fields = ['customer', 'discount']

class CustomerDiscountUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerDiscount
        fields = ['discount', 'customer']

class CustomerDiscountRetrieveSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer()
    created_by_name = serializers.CharField(source='created_by.username', read_only=True)
    modified_by_name = serializers.CharField(source='modified_by.username', read_only=True)

    class Meta:
        model = CustomerDiscount
        fields = '__all__'

class CustomerDiscountListSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer()
    created_by = serializers.CharField(source='created_by.username', read_only=True)
    modified_by = serializers.CharField(source='modified_by.username', read_only=True)

    class Meta:
        model = CustomerDiscount
        fields = '__all__'