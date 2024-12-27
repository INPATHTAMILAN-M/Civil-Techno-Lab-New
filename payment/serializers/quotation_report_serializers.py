
from django.conf import settings
from rest_framework import serializers
from ..models import QuotationReport, Quotation


class QuotationSerializer(serializers.ModelSerializer):
    quotation_file = serializers.SerializerMethodField()
    customer = serializers.StringRelatedField()
    class Meta:
        model = Quotation
        fields = '__all__'

    def get_quotation_file(self, obj):
        # Fetch the most recent QuotationReport using the related_name
        recent_report = obj.quotation_reports.order_by('-created_date').first()
        
        if recent_report and recent_report.quotation_file:
            # Build the full URL using BACKEND_DOMAIN
            full_url = f"{settings.BACKEND_DOMAIN}{recent_report.quotation_file.url}"
            return full_url
        
        return None



class QuotationReportListSerializer(serializers.ModelSerializer):
    quotation = QuotationSerializer(read_only=True)

    class Meta:
        model = QuotationReport
        fields = ['id', 'quotation', 'created_by', 'created_date', 'quotation_file']


class QuotationReportDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuotationReport
        fields = ['id', 'quotation', 'created_by', 'created_date', 'quotation_file']

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

