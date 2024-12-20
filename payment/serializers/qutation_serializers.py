from rest_framework import serializers
from payment.models import QuotationItem, Quotation
from general.models import Material, Tax

class TaxSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tax
        fields = ['id', 'tax_name', 'tax_percentage', 'tax_status', 'created_by',
                 'created_date', 'modified_by', 'modified_date']

class QuotationItemSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = QuotationItem
        fields = ['id', 'test', 'quantity', 'signature','is_authorised_signatory',
                  'created_by', 'created_date', 'modified_by', 'modified_date']

class QuotationUpdateSerializer(serializers.ModelSerializer):
    quotation_items = QuotationItemSerializer(many=True, read_only=True)
    class Meta:
        model = Quotation
        fields = ['id', 'tax', 'completed', 'quotation_items']

    

class QuotationListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quotation
        fields = ['id', 'quotation_number', 'customer', 'date_created', 'completed',
                  'total_amount', 'quotation_qr']

class QuotationRetrieveSerializer(serializers.ModelSerializer):
    tax = TaxSerializer(many=True)
    quotation_items = QuotationItemSerializer(many=True, read_only=True)

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
