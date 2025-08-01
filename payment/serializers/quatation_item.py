from rest_framework import serializers
from ..models import QuotationItem
from general.models import Test
from payment.models import Quotation
from payment.signals.quatation_signals import update_quotation_totals


class TestSerializer(serializers.ModelSerializer):
    material_name = serializers.StringRelatedField()
    created_by = serializers.StringRelatedField()
    modified_by = serializers.StringRelatedField()
    
    class Meta:
        model = Test
        fields = ['id', 'material_name', 'test_name', 'price_per_piece', 'created_by', 
                 'created_date', 'modified_by', 'modified_date']
        
class QuotationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quotation
        fields = '__all__'
        
class QuotationItemUnifiedSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuotationItem
        fields = ['quotation', 'test', 'quantity', 'signature', 'price_per_sample']

class QuotationItemBulkCreateSerializer(serializers.Serializer):
    items = QuotationItemUnifiedSerializer(many=True)

    def create(self, validated_data):
        request_user = self.context['request'].user
        items_data = validated_data.get('items', [])
        created_items = []

        for item_data in items_data:
            item_data['created_by'] = request_user  # Ensure required field is set
            item = QuotationItem(**item_data)
            item.save()  # ✅ Triggers signals and django-simple-history
            created_items.append(item)

        return created_items

class QuotationItemListSerializer(serializers.ModelSerializer):
    total_price = serializers.SerializerMethodField()
    test_name = serializers.CharField(source="test.test_name", read_only=True)
    class Meta:
        model = QuotationItem
        fields = "__all__"

    def get_total_price(self, obj):
        """Calculate the total price for this line item"""
        if obj.price_per_sample is not None:
            return obj.quantity * obj.price_per_sample
        return obj.quantity * obj.test.price_per_piece
        
class QuotationItemGetSerializer(serializers.ModelSerializer):
    test = TestSerializer()
    quotation = QuotationSerializer()
    total_price = serializers.SerializerMethodField()
    class Meta:
        model = QuotationItem
        fields = '__all__'

    def get_total_price(self, obj):
        """Calculate the total price for this line item"""
        if obj.price_per_sample is not None:
            return obj.quantity * obj.price_per_sample
        return obj.quantity * obj.test.price_per_piece
        

class QuotationItemUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuotationItem
        fields = ['test', 'quantity', 'price_per_sample']
        

class QuotationItemDeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuotationItem
        fields = ['id']