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
        
class QuotationItemUnifiedSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuotationItem
        fields = ['quotation', 'test', 'quantity', 'signature', 'price_per_sample']

class QuotationItemBulkCreateSerializer(serializers.Serializer):
    items = QuotationItemUnifiedSerializer(many=True)

    def create(self, validated_data):
        request_user = self.context['request'].user
        items_data = validated_data.get('items', [])
        for item in items_data:
            item['created_by'] = request_user

        quotation_items = [QuotationItem(**item) for item in items_data]
        return QuotationItem.objects.bulk_create(quotation_items)

class QuotationItemListSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuotationItem
        fields = ['id', 'test', 'quantity', 'signature',
                  'created_by', 'created_date', 'modified_by', 'modified_date']
        
class QuotationItemGetSerializer(serializers.ModelSerializer):
    test = TestSerializer()
    class Meta:
        model = QuotationItem
        fields = ['id', 'test', 'quantity', 'signature', 
                  'created_by', 'created_date', 'modified_by', 'modified_date']
        

class QuotationItemUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuotationItem
        fields = ['test', 'quantity']
        

class QuotationItemDeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuotationItem
        fields = ['id']