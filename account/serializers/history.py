from rest_framework import serializers

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
        try:
            previous = obj.instance.history.filter(history_date__lt=obj.history_date).order_by('-history_date').first()
        except:
            previous = None

        if not previous:
            return None

        omiting_fileds = ['id', 'history_id','history_date','modified_by','created_by','report_template',
                           'history_change_reason','created_at','modified_date','history_user']

        changes = {}
        model_fields = [f.name for f in obj._meta.fields if f.name not in omiting_fileds]
        for field in model_fields:
            old = getattr(previous, field, None)
            new = getattr(obj, field, None)
            if old != new:
                changes[field] = {
                    'from': str(old),
                    'to': str(new),
                }

        return changes or None
    
    def get_custom_info(self, obj):
        model_name = obj.instance._meta.model_name
        if model_name == "invoice_test":
            invoice = getattr(obj.instance, "invoice", None)
            return {
                "invoice_id": getattr(invoice, "id", None) if invoice else None
            }
        elif model_name == "receipt":
            invoice = getattr(obj.instance, "invoice_no", None)
            return {
                "invoice_id": getattr(invoice, "id", None) if invoice else None
            }
        elif model_name == "invoicediscount":
            invoice = getattr(obj.instance, "invoice", None)
            return {
                "invoice_id": getattr(invoice, "id", None) if invoice else None
            }
        print(model_name)
        return None
