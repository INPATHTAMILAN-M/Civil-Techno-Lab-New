from rest_framework import serializers
from payment.models.invoice_models import InvoiceDiscount
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

class InvoiceCreateSerializer(serializers.ModelSerializer):
    invoice_discounts = InvoiceDiscountSerializer(many=True, read_only=True)

    class Meta:
        model = Invoice
        fields = '__all__'


    def create(self, validated_data):
        request = self.context['request']
        validated_data['created_by'] = request.user
        validated_data['modified_by'] = request.user

        # Save initial invoice to get an ID
        invoice = super().create(validated_data)

        # 1. Generate invoice number based on financial year
        financial_year = self.get_financial_year()
        last_invoice = Invoice.objects.filter(invoice_no__endswith=f"/{financial_year}", invoice_no__isnull=False).last()
        last_invoice_no = 0
        if last_invoice:
            try:
                last_invoice_no = int(last_invoice.invoice_no.split('/')[0])
            except (ValueError, IndexError):
                last_invoice_no = 0

        next_number = last_invoice_no + 1
        prefix = f"{next_number:03d}"
        invoice_no = f"{prefix}/{financial_year}"
        invoice.invoice_no = invoice_no

        # 2. Set optional fields
        if invoice.customer.place_of_testing:
            invoice.place_of_testing = invoice.customer.place_of_testing

        invoice.date = timezone.now().date()

        # 3. Generate QR code image
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
        invoice.save()

        # 4. Generate the invoice report (PDF, HTML, etc.)
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

        # Handle tax ManyToMany field separately
        tax_data = validated_data.pop('tax', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if tax_data is not None:
            instance.tax.set(tax_data)

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

    class Meta:
        model = Invoice
        fields = '__all__'

class InvoiceListSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer(read_only=True)
    sales_mode = SalesModeSerializer(read_only=True)
    tax = TaxSerializer(many=True, read_only=True)
    
    customer_id = serializers.PrimaryKeyRelatedField(queryset=Customer.objects.all(), write_only=True, source='customer')
    sales_mode_id = serializers.PrimaryKeyRelatedField(queryset=SalesMode.objects.all(), write_only=True, source='sales_mode')
    tax_ids = serializers.PrimaryKeyRelatedField(queryset=Tax.objects.all(), many=True, write_only=True, source='tax')
    
    class Meta:
        model = Invoice
        fields = '__all__'
