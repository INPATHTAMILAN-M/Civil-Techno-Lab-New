from rest_framework import serializers
from payment.models.invoice_models import Expense_Entry


class Expense_Entry_Serializer(serializers.ModelSerializer):
    created_by = serializers.StringRelatedField()
    modified_by = serializers.StringRelatedField()
    expense_category_name = serializers.SerializerMethodField()

    class Meta:
        model = Expense_Entry
        fields = ['id','expense_user','date','amount','expense_category','narration',
                  'created_by','created_date','modified_by','modified_date','expense_category_name']

    def get_expense_category_name(self,obj):
        return str(obj.expense_category)
    