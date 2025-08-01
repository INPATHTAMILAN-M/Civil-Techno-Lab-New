from rest_framework import serializers
from payment.models.invoice_models import InvoiceDiscount, Receipt
from payment.models import Invoice, SalesMode, CustomerDiscount
from general.models import Tax
from account.models import Customer

from utils.generate_invoice import generate_invoice_report
import qrcode
import os
from django.conf import settings
from django.utils import timezone
from django.contrib.auth import get_user_model
User = get_user_model()

class InvoiceDiscountSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvoiceDiscount
        fields = '__all__'


class CustomerDiscountSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerDiscount
        fields = '__all__'

class CustomerSerializer(serializers.ModelSerializer):
    customer_discount = CustomerDiscountSerializer(read_only=True)
    class Meta:
        model = Customer
        fields = "__all__"

class SalesModeSerializer(serializers.ModelSerializer):
    class Meta:
        model = SalesMode
        fields = "__all__"

class TaxSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tax
        fields = "__all__"

class InvoiceReceiptSerializer(serializers.ModelSerializer):
    class Meta:
        model = Receipt
        fields = '__all__'

class InvoiceCreateSerializer(serializers.ModelSerializer):
    invoice_discounts = InvoiceDiscountSerializer(many=True, read_only=True)

    class Meta:
        model = Invoice
        fields = '__all__'

    def create(self, validated_data):
        request = self.context['request']
        validated_data.update({
            'created_by': request.user,
            'modified_by': request.user,
            'date': timezone.now().date(),
        })

        # Set place of testing if available
        if 'customer' in validated_data and validated_data['customer'].place_of_testing:
            validated_data['place_of_testing'] = validated_data['customer'].place_of_testing

        # Generate invoice number
        financial_year = self.get_financial_year()
        last_invoice = Invoice.objects.filter(
            invoice_no__endswith=f"/{financial_year}", 
            invoice_no__isnull=False
        ).last()
        
        last_invoice_no = 0
        if last_invoice:
            try:
                last_invoice_no = int(last_invoice.invoice_no.split('/')[0])
            except (ValueError, IndexError):
                pass

        next_number = last_invoice_no + 1
        prefix = f"{next_number:03d}"
        validated_data['invoice_no'] = f"{prefix}/{financial_year}"

        # Create invoice with all data at once
        invoice = super().create(validated_data)

        # Generate QR code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(f"{settings.QR_DOMAIN}/invoice/viewinvoicereport?id={invoice.id}")
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")

        invoice_img_dir = "media/invoice"
        os.makedirs(invoice_img_dir, exist_ok=True)
        invoice_img_filename = f"invoice_{prefix}-{financial_year}.png"
        invoice_img_path = os.path.join(invoice_img_dir, invoice_img_filename)
        img.save(invoice_img_path)

        invoice.invoice_image = invoice_img_path

        # Generate invoice report after creation
        generate_invoice_report(invoice, request)

        return invoice

    def get_financial_year(self):
        now = timezone.now()
        year = now.year
        month = now.month
        if month >= 4:
            fy_start = year
            fy_end = year + 1
        else:
            fy_start = year - 1
            fy_end = year
        return f"{str(fy_start)[2:]}-{str(fy_end)[2:]}"


class InvoiceUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invoice
        fields = '__all__'

    def update(self, instance, validated_data):
        request = self.context['request']
        validated_data['modified_by'] = request.user

        tax_data = validated_data.pop('tax', None)
        updated_fields = []

        # Check and update only changed fields
        for attr, new_value in validated_data.items():
            old_value = getattr(instance, attr)
            if old_value != new_value:
                setattr(instance, attr, new_value)
                updated_fields.append(attr)

        if updated_fields:
            instance.save(update_fields=updated_fields)

        # Handle ManyToMany (tax)
        if tax_data is not None:
            old_tax_ids = set(instance.tax.values_list('id', flat=True))
            new_tax_ids = set([t.id if hasattr(t, 'id') else t for t in tax_data])
            if old_tax_ids != new_tax_ids:
                instance.tax.set(tax_data)

        # Always regenerate report (if needed for preview update)
        generate_invoice_report(instance, request)

        return instance

class InvoiceRetrieveSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer(read_only=True)
    sales_mode = SalesModeSerializer(read_only=True)
    tax = TaxSerializer(many=True, read_only=True)
    
    customer_id = serializers.PrimaryKeyRelatedField(queryset=Customer.objects.all(), write_only=True, source='customer')
    sales_mode_id = serializers.PrimaryKeyRelatedField(queryset=SalesMode.objects.all(), write_only=True, source='sales_mode')
    tax_ids = serializers.PrimaryKeyRelatedField(queryset=Tax.objects.all(), many=True, write_only=True, source='tax')
    invoice_discounts = InvoiceDiscountSerializer(many=True, read_only=True)
    invoice_file = serializers.SerializerMethodField()
    invoice_receipts = InvoiceReceiptSerializer(many=True, read_only=True)

    class Meta:
        model = Invoice
        fields = '__all__'

    def get_invoice_file(self, obj):
        # Fetch the most recent QuotationReport using the related_name
        recent_report = obj.invoice_reports.order_by('-id').first()
        
        if recent_report and recent_report.invoice_file:
            # Build the full URL using BACKEND_DOMAIN
            full_url = f"{settings.BACKEND_DOMAIN}{recent_report.invoice_file.url}"
            return full_url
        
        return None

class InvoiceListSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer(read_only=True)
    sales_mode = SalesModeSerializer(read_only=True)
    tax = TaxSerializer(many=True, read_only=True)
    
    customer_id = serializers.PrimaryKeyRelatedField(queryset=Customer.objects.all(), write_only=True, source='customer')
    sales_mode_id = serializers.PrimaryKeyRelatedField(queryset=SalesMode.objects.all(), write_only=True, source='sales_mode')
    tax_ids = serializers.PrimaryKeyRelatedField(queryset=Tax.objects.all(), many=True, write_only=True, source='tax')
    invoice_file = serializers.SerializerMethodField()
    invoice_receipt = serializers.SerializerMethodField()
    
    class Meta:
        model = Invoice
        fields = '__all__'

    def get_invoice_file(self, obj):
        recent_report = obj.invoice_reports.order_by('-id').first()
        
        if recent_report and recent_report.invoice_file:
            full_url = f"{settings.BACKEND_DOMAIN}{recent_report.invoice_file.url}"
            return full_url
        
        return None
    
    def get_invoice_receipt(self, obj):
        last_receipt = Receipt.objects.filter(invoice_no=obj).order_by('-created_date').first()
        
        if last_receipt:
            return InvoiceReceiptSerializer(last_receipt).data

        return None

    




    

    