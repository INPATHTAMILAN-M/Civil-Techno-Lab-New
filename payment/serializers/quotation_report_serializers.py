
from rest_framework import serializers
from ..models import QuotationReport

class QuotationReportListSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuotationReport
        fields = ['id', 'quotation', 'created_by', 'created_date']


class QuotationReportDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuotationReport
        fields = ['id', 'quotation', 'created_by', 'created_date']

class QuotationReportCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuotationReport
        fields = ['quotation']

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['created_by'] = user
        return super().create(validated_data)

class QuotationReportUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuotationReport
        fields = ['quotation_file']

