from rest_framework import serializers
from django.core.exceptions import ObjectDoesNotExist

class HistorySerializer(serializers.Serializer):
    id = serializers.IntegerField(source='instance.id')
    history_id = serializers.IntegerField()
    history_date = serializers.DateTimeField()
    history_user = serializers.StringRelatedField()
    is_admin = serializers.SerializerMethodField()
    history_type = serializers.CharField()
    history_change_reason = serializers.CharField(allow_null=True, required=False)
    history_action = serializers.SerializerMethodField()
    changes = serializers.SerializerMethodField()
    custom_info = serializers.SerializerMethodField()

    def get_history_action(self, obj):
        return {
            '+': 'Created',
            '~': 'Updated',
            '-': 'Deleted'
        }.get(obj.history_type, 'Unknown')

    def get_is_admin(self, obj):
        user = obj.history_user
        if user and user.is_authenticated:
            return user.is_superuser or user.groups.filter(name="Admin").exists()
        return False

    def get_changes(self, obj):
        prev = obj.prev_record
        if not prev:
            return {}

        delta = obj.diff_against(prev, foreign_keys_are_objs=True)
        OMIT_FIELDS = ['updated_at', 'created_at', 'last_login','Report_template'] 

        def safe_value(value):
            # Convert FK objects to strings (e.g., __str__) or IDs
            if hasattr(value, '__str__'):
                return str(value)
            return value

        return {
            change.field: {
                'from': safe_value(change.old),
                'to': safe_value(change.new)
            }
            for change in delta.changes  if change.field not in OMIT_FIELDS
        }

    def get_custom_info(self, obj):
        
        model_name = obj.instance._meta.model_name
        if model_name == "invoice_test":
            try:
                invoice = obj.instance.invoice
                invoice_id = invoice.id if invoice else None
            except ObjectDoesNotExist:
                invoice_id = None
            return {"invoice_id": invoice_id}

        elif model_name == "receipt":
            try:
                invoice = obj.instance.invoice_no
                invoice_id = invoice.id if invoice else None
            except ObjectDoesNotExist:
                invoice_id = None
            return {"invoice_id": invoice_id}

        elif model_name == "invoicediscount":
            try:
                invoice = obj.instance.invoice
                invoice_id = invoice.id if invoice else None
            except ObjectDoesNotExist:
                invoice_id = None
            return {"invoice_id": invoice_id}

        elif model_name == "quotationitem":
            try:
                quotation = obj.instance.quotation
                quotation_id = quotation.id if quotation else None
            except ObjectDoesNotExist:
                quotation_id = None
            return {"quotation_id": quotation_id}

        elif model_name == "user":
            try:
                employee = obj.instance.employee_user
                employee_id = employee.id if employee else None
            except ObjectDoesNotExist:
                employee_id = None
            return {"employee_id": employee_id}
        return None