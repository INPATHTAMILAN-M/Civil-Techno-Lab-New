from rest_framework import serializers
from general.models import Test,Material

class MaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Material
        fields = '__all__'

class TestSerializer(serializers.ModelSerializer):
    material = MaterialSerializer(read_only=True)
    class Meta:
        model = Test
        fields = '__all__'

