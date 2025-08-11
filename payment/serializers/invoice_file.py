
from rest_framework import serializers
from django.conf import settings
from payment.models import Invoice_File  

class InvoiceFileBaseSerializer(serializers.ModelSerializer):
    created_by = serializers.StringRelatedField(read_only=True)
    modified_by = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Invoice_File
        fields = ['id', 'invoice', 'category', 'created_by', 'modified_by', 
                  'created_date', 'modified_date', 'expense']


class InvoiceFileCreateSerializer(InvoiceFileBaseSerializer):
    class Meta(InvoiceFileBaseSerializer.Meta):
        read_only_fields = ['created_by', 'modified_by', 'created_date', 'modified_date']


class InvoiceFileUpdateSerializer(InvoiceFileBaseSerializer):
    class Meta(InvoiceFileBaseSerializer.Meta):
        read_only_fields = ['created_by', 'modified_by', 'created_date', 'modified_date']



class InvoiceFileRetrieveSerializer(InvoiceFileBaseSerializer):
    file_url = serializers.SerializerMethodField()
    invoice_no = serializers.SerializerMethodField()
    category_name = serializers.SerializerMethodField()
    expense_category = serializers.SerializerMethodField()
    expense_user = serializers.SerializerMethodField()
    expence_amount = serializers.IntegerField(source='expense.amount', read_only=True)
    invoice_amount = serializers.IntegerField(source='invoice.total_amount', read_only=True)
    customer = serializers.CharField(source='invoice.customer.customer_name', read_only=True)
    customer_number = serializers.CharField(source='invoice.customer.phone_no', read_only=True)
    project_name = serializers.CharField(source='invoice.project_name', read_only=True)

    class Meta(InvoiceFileBaseSerializer.Meta):
        fields = InvoiceFileBaseSerializer.Meta.fields + [
            'file_url', 'invoice_no', 'category_name', 'expense_category', 
            'expense_user','expence_amount','invoice_amount', 'customer', 'project_name','customer_number'
        ]

    def get_invoice_no(self, obj):
        return getattr(obj.invoice, "invoice_no", None)

    def get_category_name(self, obj):
        return str(obj.category)

    def get_expense_category(self, obj):
        try:
            return str(obj.expense.expense_category.expense_name)
        except:
            return None

    def get_expense_user(self, obj):
        try:
            return str(obj.expense.expense_user)
        except:
            return None

    def get_file_url(self, obj):
        return f"{settings.BACKEND_DOMAIN}/media/{obj.file}"


class InvoiceFileListSerializer(InvoiceFileBaseSerializer):
    file_url = serializers.SerializerMethodField()
    invoice_no = serializers.SerializerMethodField()
    category_name = serializers.SerializerMethodField()
    expense_category = serializers.SerializerMethodField()
    expense_user = serializers.SerializerMethodField()
    expence_amount = serializers.IntegerField(source='expense.amount', read_only=True)
    invoice_amount = serializers.IntegerField(source='invoice.total_amount', read_only=True)
    customer = serializers.CharField(source='invoice.customer.customer_name', read_only=True)
    project_name = serializers.CharField(source='invoice.project_name', read_only=True)
    customer_number = serializers.CharField(source='invoice.customer.phone_no', read_only=True)

    class Meta(InvoiceFileBaseSerializer.Meta):
        fields = InvoiceFileBaseSerializer.Meta.fields + [
            'file_url', 'invoice_no', 'category_name', 'expense_category', 
            'expense_user','expence_amount','invoice_amount','customer', 'project_name',
            'customer_number'
        ]

    def get_invoice_no(self, obj):
        return getattr(obj.invoice, "invoice_no", None)

    def get_category_name(self, obj):
        return str(obj.category)

    def get_expense_category(self, obj):
        try:
            return str(obj.expense.expense_category.expense_name)
        except:
            return None

    def get_expense_user(self, obj):
        try:
            return str(obj.expense.expense_user)
        except:
            return None

    def get_file_url(self, obj):
        return f"{settings.BACKEND_DOMAIN}/media/{obj.file}"