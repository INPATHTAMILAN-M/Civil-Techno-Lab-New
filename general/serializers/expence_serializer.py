from rest_framework import serializers
from django.contrib.auth.models import User
from ..models import Expense


class Expense_Serializer(serializers.ModelSerializer):
    created_by = serializers.StringRelatedField()
    modified_by = serializers.StringRelatedField()
    class Meta:
        model = Expense
        fields = ['id', 'expense_name', 'created_by', 'created_date', 'modified_by', 'modified_date']

