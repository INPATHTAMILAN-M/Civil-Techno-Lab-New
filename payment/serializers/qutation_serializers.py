from rest_framework import serializers
from payment.models import QuotationItem, Quotation, QuotationReport
from general.models import Material, Tax
from account.models import Customer


class CustomerSerializer(serializers.ModelSerializer):
    created_by = serializers.StringRelatedField()
    modified_by = serializers.StringRelatedField()
    city1 = serializers.StringRelatedField()
    state1 = serializers.StringRelatedField()
    country1 = serializers.StringRelatedField()
    city2 = serializers.StringRelatedField()
    state2 = serializers.StringRelatedField()
    country2 = serializers.StringRelatedField()

    class Meta:
        model = Customer
        fields = ('customer_name', 'phone_no', 'gstin_no', 'email', 'address1',
                 'city1', 'state1', 'country1', 'pincode1', 'contact_person1',
                 'mobile_no1', 'contact_person_email1', 'place_of_testing',
                 'address2', 'city2', 'state2', 'country2', 'pincode2',
                 'contact_person2', 'mobile_no2', 'contact_person_email2',
                 'created_by', 'created_date', 'modified_by', 'modified_date')

class TaxSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tax
        fields = ['id', 'tax_name', 'tax_percentage', 'tax_status', 'created_by',
                 'created_date', 'modified_by', 'modified_date']

class QuotationItemSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = QuotationItem
        fields = ['id', 'test', 'quantity', 'signature',
                  'created_by', 'created_date', 'modified_by', 'modified_date']

class QuotationUpdateSerializer(serializers.ModelSerializer):
    quotation_items = QuotationItemSerializer(many=True, read_only=True)
    class Meta:
        model = Quotation
        fields = ['id', 'tax', 'completed', 'quotation_items']

    
    def update(self, instance, validated_data):
        if validated_data.get("completed"):
            QuotationReport.objects.create(quotation=instance, created_by=self.context['request'].user)
        return super().update(instance, validated_data)
    

class QuotationListSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Quotation
        fields = ['id', 'quotation_number', 'customer', 'date_created', 'completed',
                  'total_amount', 'quotation_qr']

class QuotationRetrieveSerializer(serializers.ModelSerializer):
    tax = TaxSerializer(many=True)
    quotation_items = QuotationItemSerializer(many=True, read_only=True)
    customer = CustomerSerializer()

    class Meta:
        model = Quotation
        fields = ['id', 'quotation_number', 'customer', 'date_created', 'tax', 
                  'completed','total_amount', 'quotation_items', 'quotation_qr']
        
class QuotationCreateSerializer(serializers.ModelSerializer):
    quotation_qr = serializers.ImageField(read_only=True)
    class Meta:
        model = Quotation
        fields = ['customer', 'tax', 'quotation_qr' ]
        
class QuotationSerializer(serializers.ModelSerializer):
    quotation_items = QuotationItemSerializer(many=True, read_only=True)
    class Meta:
        model = Quotation
        fields = ['id', 'customer', 'quotation_number', 'date_created', 'tax', 
                  'quotation_qr', 'completed', 'total_amount', 'quotation_items']
