
from django.conf import settings
from rest_framework import serializers
from payment.models import InvoiceReport, Invoice, Invoice_Test
from general.models import Tax
from account.models import Customer

class TaxSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tax
        fields = ['id', 'tax_name', 'tax_percentage', 'tax_status', 'created_by',
                 'created_date', 'modified_by', 'modified_date']
        
class CustomerSerializer(serializers.ModelSerializer):
    created_by = serializers.StringRelatedField()
    modified_by = serializers.StringRelatedField()
    city1 = serializers.StringRelatedField()
    state1 = serializers.StringRelatedField()
    country1 = serializers.StringRelatedField()
    city2 = serializers.StringRelatedField()
    state2 = serializers.StringRelatedField()
    country2 = serializers.StringRelatedField()

    class Meta:
        model = Customer
        fields = ('customer_name', 'phone_no', 'gstin_no', 'email', 'address1',
                 'city1', 'state1', 'country1', 'pincode1', 'contact_person1',
                 'mobile_no1', 'contact_person_email1', 'place_of_testing',
                 'address2', 'city2', 'state2', 'country2', 'pincode2',
                 'contact_person2', 'mobile_no2', 'contact_person_email2',
                 'created_by', 'created_date', 'modified_by', 'modified_date')



class InvoiceTestSerializer(serializers.ModelSerializer):
    created_by = serializers.StringRelatedField()
    modified_by = serializers.StringRelatedField()
    signature = serializers.StringRelatedField()
    test = serializers.StringRelatedField()
    customer = serializers.StringRelatedField()

    class Meta:
        model = Invoice_Test
        fields = ('customer', 'test', 'quantity', 'total', 
                 'price_per_sample', 'report_template', 'invoice_image', 
                 'completed', 'signature', 'is_authorised_signatory', 
                 'created_by', 'created_date', 'modified_by', 'modified_date',
                 'ulr')

class InvoiceListSerializer(serializers.ModelSerializer):
    customer = serializers.StringRelatedField()
    invoice_file = serializers.SerializerMethodField()

    class Meta:
        model = Invoice
        fields = ('id','customer', 'sales_mode', 'project_name', 'discount', 'tax', 
                 'advance', 'balance', 'total_amount', 'tds_amount', 'fully_paid',
                 'date', 'invoice_no', 'payment_mode', 'cheque_number', 'upi',
                 'bank', 'amount_paid_date', 'invoice_image', 'place_of_testing',
                 'completed', 'is_old_invoice_format', "invoice_tests",'invoice_file')
        
    def get_invoice_file(self, obj):
        # Fetch the most recent QuotationReport using the related_name
        recent_report = obj.invoice_reports.order_by('-id').first()
        
        if recent_report and recent_report.invoice_file:
            # Build the full URL using BACKEND_DOMAIN
            full_url = f"{settings.BACKEND_DOMAIN}{recent_report.invoice_file.url}"
            return full_url
        
        return None



class InvoiceSerializer(serializers.ModelSerializer):
    invoice_tests = InvoiceTestSerializer(many=True)
    tax = TaxSerializer(many=True)
    customer = CustomerSerializer()

    class Meta:
        model = Invoice
        fields = ('customer', 'sales_mode', 'project_name', 'discount', 'tax', 
                 'advance', 'balance', 'total_amount', 'tds_amount', 'fully_paid',
                 'date', 'invoice_no', 'payment_mode', 'cheque_number', 'upi',
                 'bank', 'amount_paid_date', 'invoice_image', 'place_of_testing',
                 'completed', 'is_old_invoice_format', "invoice_tests")



class InvoiceReportCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvoiceReport
        fields = ('invoice', 'invoice_file')

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['created_by'] = user
        validated_data['modified_by'] = user
        return super().create(validated_data)

class InvoiceReportUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvoiceReport
        fields = ('invoice_file',)

    def update(self, instance, validated_data):
        user = self.context['request'].user
        validated_data['modified_by'] = user
        return super().update(instance, validated_data)

class InvoiceReportListSerializer(serializers.ModelSerializer):
    
    invoice = InvoiceListSerializer()
    class Meta:
        model = InvoiceReport
        fields = ('id', 'invoice', 'created_by', 'created_date')


class InvoiceReportDetailSerializer(serializers.ModelSerializer):
    invoice = InvoiceSerializer()
    class Meta:
        model = InvoiceReport
        fields = ('id', 'invoice', 'created_by', 'created_date','invoice_file')
