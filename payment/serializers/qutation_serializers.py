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
        fields = ['id', 'tax', 'completed','customer','quotation_items']


    def update(self, instance, validated_data):
        if validated_data.get("completed"):
            import os
            from django.template.loader import render_to_string
            from weasyprint import HTML
            from django.conf import settings
            from django.db.models import Sum
            from ..models import QuotationReport

            # Refresh the instance to get the most recent data
            instance.refresh_from_db()

            context = {
                'quotation': validated_data.get('quotation', instance),                
                'customer': instance.customer,
                'quotation_items': instance.quotation_items.all(),
                'sub_total': instance.sub_total,
                'tax': validated_data.get('tax', []),
                'tax_total': sum(tax.tax_percentage for tax in validated_data.get('tax', [])) or 0,  # Sum tax percentages using dot notation
                'tax_display': "+".join(f"{tax.tax_name} ({tax.tax_percentage}%)" for tax in validated_data.get('tax', [])),
                "settings": settings
            }

            html_content = render_to_string('quotation.html', context)
            pdf_file = HTML(string=html_content).write_pdf()
            
            # Set up the file path and save the PDF file
            pdf_dir = os.path.join(settings.MEDIA_ROOT, 'quotations')
            os.makedirs(pdf_dir, exist_ok=True)
            file_path = os.path.join(pdf_dir, f"quotation_{instance.id}.pdf")
            
            with open(file_path, 'wb') as f:
                f.write(pdf_file)
            
            # Update the instance's pdf_path and save it
            instance.pdf_path = file_path
            instance.save()

            # Update or create the QuotationReport entry
            QuotationReport.objects.update_or_create(
                quotation=instance, 
                created_by=instance.created_by,  # Use `created_by` or another user-tracking field
                defaults={
                    'quotation_file': f"/quotations/quotation_{instance.id}.pdf"
                }
            )

        # Continue with the default update behavior
        return super().update(instance, validated_data)

    

class QuotationListSerializer(serializers.ModelSerializer):
    customer = serializers.CharField(source='customer.customer_name', read_only=True)

    class Meta:
        model = Quotation
        fields = ['id', 'quotation_number', 'customer', 'date_created', 'completed',
                  'total_amount', 'quotation_qr']
        
class CustomerListSerializer(serializers.ModelSerializer):
    # customer_name = serializers.CharField(source='name')  # Assuming 'name' is the field in Customer model

    class Meta:
        model = Customer
        fields = ['id', 'customer_name', 'address1', 'phone_no']

class QuotationRetrieveSerializer(serializers.ModelSerializer):
    tax = serializers.SerializerMethodField() 
    quotation_items = QuotationItemSerializer(many=True, read_only=True)
    customer = CustomerSerializer()
    customer_list = serializers.SerializerMethodField()
    total_amount = serializers.SerializerMethodField()
    tax_list = serializers.SerializerMethodField()

    class Meta:
        model = Quotation
        fields = ['id', 'quotation_number', 'customer', 'date_created', 'tax', 
                  'completed','total_amount', 'quotation_items', 'quotation_qr','customer_list','tax_list']
        

    def get_tax(self, obj):
        tax_list = []
        for tax in obj.tax.all():
            tax_list.append(tax.id)
        return tax_list
    

    def get_customer_list(self, obj):
        # Get all customers and serialize them using CustomerListSerializer
        customers = Customer.objects.all()
        return CustomerListSerializer(customers, many=True).data
    
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
