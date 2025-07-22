from rest_framework import serializers
from general.models import Material, Test
from django.utils import timezone

class MaterialBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Material
        fields = [
            'id',
            'material_name',
            'template',
            'created_by',
            'created_date',
            'modified_by',
            'modified_date',
            'print_format',
            'letter_pad_logo',
        ]


class TestBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Test
        fields = '__all__'

class TestCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Test
        fields = ['material_name', 'test_name', 'price_per_piece']

    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user
        return super().create(validated_data)


class TestUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Test
        fields = ['material_name', 'test_name', 'price_per_piece']

    def update(self, instance, validated_data):
        instance.modified_by = self.context['request'].user
        instance.modified_date = timezone.now()
        return super().update(instance, validated_data)


class TestDetailSerializer(serializers.ModelSerializer):
    material_name = MaterialBaseSerializer(read_only=True)
    created_by = serializers.StringRelatedField()
    modified_by = serializers.StringRelatedField()

    class Meta:
        model = Test
        fields = '__all__'


class TestListSerializer(serializers.ModelSerializer):
    material_name = MaterialBaseSerializer(read_only=True)
    class Meta:
        model = Test
        fields = ['id', 'test_name', 'material_name', 'price_per_piece']