from rest_framework import serializers
from general.models import Tax

        
class TaxListSerializer(serializers.ModelSerializer):
    status = serializers.SerializerMethodField()

    class Meta:
        model = Tax
        fields = ['id','tax_name','tax_percentage', 'tax_status', 'status', 'created_by', 'created_date', 'modified_by', 'modified_date']

    def get_status(self, obj):
        return "Enable" if obj.tax_status == 'E' else "Disable"
    