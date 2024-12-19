from rest_framework import serializers
from ..models import QuotationItem
from general.models import Test


class TestSerializer(serializers.ModelSerializer):
    material_name = serializers.StringRelatedField()
    created_by = serializers.StringRelatedField()
    modified_by = serializers.StringRelatedField()
    
    class Meta:
        model = Test
        fields = ['id', 'material_name', 'test_name', 'price_per_piece', 'created_by', 
                 'created_date', 'modified_by', 'modified_date']
        
class QuotationItemCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuotationItem
        fields = ['quotation','test', 'quantity', 'quotation_image', 'signature', 
                  'is_authorised_signatory', 'created_by']
        
class QuotationItemListSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuotationItem
        fields = ['id', 'test', 'quantity', 'quotation_image', 'signature', 
                  'is_authorised_signatory', 'created_by', 'created_date', 'modified_by', 'modified_date']
        
class QuotationItemGetSerializer(serializers.ModelSerializer):
    test = TestSerializer()
    class Meta:
        model = QuotationItem
        fields = ['id', 'test', 'quantity', 'quotation_image', 'signature', 
                  'is_authorised_signatory', 'created_by', 'created_date', 'modified_by', 'modified_date']
        

class QuotationItemUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuotationItem
        fields = ['test', 'quantity', 'quotation_image', 'signature', 
                  'is_authorised_signatory']