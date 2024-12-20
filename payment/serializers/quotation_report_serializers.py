
from rest_framework import serializers
from ..models import QuotationReport

class QuotationReportListSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuotationReport
        fields = ['id', 'quotation', 'quotation_file', 'created_by', 'created_date']

class QuotationReportDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuotationReport
        fields = ['id', 'quotation', 'quotation_file', 'created_by', 'created_date', 'modified_by', 'modified_date']

class QuotationReportCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuotationReport
        fields = ['quotation', 'quotation_file']

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['created_by'] = user
        validated_data['modified_by'] = user
        return super().create(validated_data)

class QuotationReportUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuotationReport
        fields = ['quotation_file']

    def update(self, instance, validated_data):
        validated_data['modified_by'] = self.context['request'].user
        return super().update(instance, validated_data)
