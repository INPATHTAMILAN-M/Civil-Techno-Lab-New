from decimal import Decimal
from rest_framework import serializers
from payment.models import Receipt,Invoice

class invoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invoice
        fields = '__all__'

class ReceiptListSerializer(serializers.ModelSerializer):
    invoice_no = invoiceSerializer(read_only=True)

    class Meta:
        model = Receipt
        fields = '__all__'

class ReceiptCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Receipt
        fields = '__all__'


class ReceiptDetailSerializer(serializers.ModelSerializer):
    invoice_no = invoiceSerializer(read_only=True)

    class Meta:
        model = Receipt
        fields = '__all__'

class ReceiptUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Receipt
        fields = '__all__'


    def validate(self, attrs):
        invoice = attrs.get("invoice_no", getattr(self.instance, "invoice_no"))
        new_amount = Decimal(attrs.get("amount", getattr(self.instance, "amount", 0)))
        
        # Get all other receipts
        other_receipts = Receipt.objects.filter(invoice_no=invoice).exclude(pk=self.instance.pk)

        # Calculate totals
        other_payments = sum((r.amount or 0) for r in other_receipts)

        if other_payments == 0:
            max_allowed = invoice.after_tax_amount

        else:
            max_allowed = invoice.after_tax_amount - other_payments
        
        if new_amount > max_allowed:
            raise serializers.ValidationError({
                "amount": f"You can only update payment up to ₹{max_allowed:.2f} on this invoice"
            })
        
        return attrs



