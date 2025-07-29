import os
from django.template.loader import render_to_string
from weasyprint import HTML
from django.conf import settings
from django.db.models import Sum
from ..models import QuotationReport


from rest_framework import serializers
from payment.models import QuotationItem, Quotation, QuotationReport
from general.models import Tax
from account.models import Customer
from django.conf import settings


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
        fields = ('id','customer_name', 'phone_no', 'gstin_no', 'email', 'address1',
                 'city1', 'state1', 'country1', 'pincode1', 'contact_person1',
                 'mobile_no1', 'contact_person_email1', 'place_of_testing',
                 'address2', 'city2', 'state2', 'country2', 'pincode2',
                 'contact_person2', 'mobile_no2', 'contact_person_email2',
                 'created_by', 'created_date', 'modified_by', 'modified_date')

class TaxSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tax
        fields = ['id', 'tax_name', 'tax_percentage', 'tax_status', 'created_by',
                 'created_date', 'modified_by', 'modified_date']

class QuotationItemSerializer(serializers.ModelSerializer):
    total = serializers.SerializerMethodField()
    test = serializers.CharField(source='test.test_name', read_only=True)
    test_id = serializers.IntegerField(source='test.id', read_only=True)
    class Meta:
        model = QuotationItem
        fields = ['id', 'test', 'test_id', 'quantity', 'signature', 'price_per_sample',
                  'created_by', 'created_date', 'modified_by', 'modified_date', 'total']

    def get_total(self, obj):
        if obj.price_per_sample:
            return obj.quantity * obj.price_per_sample
        return 0
    
class QuotationUpdateSerializer(serializers.ModelSerializer):
    quotation_items = QuotationItemSerializer(many=True, read_only=True)
    class Meta:
        model = Quotation
        fields = ['id', 'tax', 'completed','customer','quotation_items','date_created']


    def update(self, instance, validated_data):

        # Extract and remove tax from validated_data (handle M2M separately)
        tax_data = validated_data.pop('tax', None)

        # Update simple fields only if changed
        has_changes = False
        for attr, value in validated_data.items():
            old_value = getattr(instance, attr)
            if old_value != value:
                setattr(instance, attr, value)
                has_changes = True

        # Handle tax M2M
        if tax_data is not None:
            old_tax_ids = set(instance.tax.values_list('id', flat=True))
            new_tax_ids = set([t.id if hasattr(t, 'id') else t for t in tax_data])
            if old_tax_ids != new_tax_ids:
                instance.tax.set(tax_data)
                has_changes = True

        # Only save if anything changed
        if has_changes:
            instance.save()

        # Generate PDF regardless of whether fields changed
        tax_set = instance.tax.all()
        sub_total = instance.sub_total or 0
        tax_total = sum(t.tax_percentage for t in tax_set)
        tax_display = " + ".join(f"{t.tax_name} ({t.tax_percentage}%)" for t in tax_set)

        context = {
            'quotation': instance,
            'customer': instance.customer,
            'quotation_items': instance.quotation_items.all(),
            'sub_total': sub_total,
            'tax': tax_set,
            'tax_total': tax_total,
            'tax_display': tax_display,
            'settings': settings,
        }

        html_content = render_to_string('quotation.html', context)
        pdf_file = HTML(string=html_content).write_pdf()

        # Save PDF file
        pdf_dir = os.path.join(settings.MEDIA_ROOT, 'quotations')
        os.makedirs(pdf_dir, exist_ok=True)
        pdf_filename = f"quotation_{instance.id}.pdf"
        file_path = os.path.join(pdf_dir, pdf_filename)

        with open(file_path, 'wb') as f:
            f.write(pdf_file)

        # Update PDF path if changed
        relative_path = f"quotations/{pdf_filename}"

        # Update or create the QuotationReport entry
        QuotationReport.objects.update_or_create(
            quotation=instance,
            defaults={'quotation_file': f"/{relative_path}"}
        )

        return instance

    

class QuotationListSerializer(serializers.ModelSerializer):
    customer = serializers.CharField(source='customer.customer_name', read_only=True)
    class Meta:
        model = Quotation
        fields = "__all__"
        
class CustomerListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['id', 'customer_name', 'address1', 'phone_no']

from rest_framework import serializers
from general.models import Tax

        
class TaxListSerializer(serializers.ModelSerializer):
    status = serializers.SerializerMethodField()

    class Meta:
        model = Tax
        fields = ['id','tax_name','tax_percentage', 'tax_status', 'status', 'created_by', 'created_date', 'modified_by', 'modified_date']

    def get_status(self, obj):
        return "Enable" if obj.tax_status == 'E' else "Disable"
    

class QuotationRetrieveSerializer(serializers.ModelSerializer):
    quotation_items = QuotationItemSerializer(many=True, read_only=True)
    customer = CustomerSerializer()
    total_amount = serializers.SerializerMethodField()
    tax = TaxListSerializer(many=True)

    class Meta:
        model = Quotation
        fields = ['id', 'quotation_number', 'customer', 'date_created', 'tax', 'completed',
                  'total_amount', 'quotation_items', 'quotation_qr','before_tax','after_tax',
                  'total_amount']
    
    def get_total_amount(self, obj):
        # Calculate the base total amount for all quotation items (without tax)
        base_total = 0
        
        for item in obj.quotation_items.all():
            price = float(item.price_per_sample or 0)  # Ensure it's a float
            base_total += item.quantity * price

        return round(base_total, 2)


    def to_representation(self, instance):
        representation = super().to_representation(instance)
        # Add tax details dynamically to the final response
        tax_details = self.context.get('tax_details', {})
        representation.update(tax_details)

        return representation
    
    def get_tax_list(self, obj):
        # Gather all related tax objects
        taxes = Tax.objects.filter(tax_status="E") 
        return TaxSerializer(taxes, many=True).data
        
class QuotationCreateSerializer(serializers.ModelSerializer):
    quotation_qr = serializers.ImageField(read_only=True)
    class Meta:
        model = Quotation
        fields = ['id','customer', 'tax', 'quotation_qr' ]
        
class QuotationSerializer(serializers.ModelSerializer):
    quotation_items = QuotationItemSerializer(many=True, read_only=True)
    class Meta:
        model = Quotation
        fields = ['id', 'customer', 'quotation_number', 'date_created', 'tax', 
                  'quotation_qr', 'completed', 'total_amount', 'quotation_items']
