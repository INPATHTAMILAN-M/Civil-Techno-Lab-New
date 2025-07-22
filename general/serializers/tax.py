from rest_framework import serializers
from general.models import Tax

        
class TaxSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tax
        fields = '__all__'


    