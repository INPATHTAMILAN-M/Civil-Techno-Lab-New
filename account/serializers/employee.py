from rest_framework import serializers
from account.models import Employee
from django.conf import settings

class Create_Employee_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ['employee_name','address','mobile_number',
                  'email','dob','gender','qualification','joining_date',
                  'salary','signature','branch_email','role','is_active']

class Employee_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ['id','employee_name','address','mobile_number',
                  'email','dob','gender','qualification','joining_date',
                  'salary','branch_email','role']

class Employee_List_Serializer(serializers.ModelSerializer):
    created_by = serializers.StringRelatedField()
    modified_by = serializers.StringRelatedField()
    username = serializers.SerializerMethodField()
    gender_name = serializers.SerializerMethodField()
    signature = serializers.SerializerMethodField()
    
    class Meta:
        model = Employee
        fields = ['id','username','employee_name','address','mobile_number',
                  'email','dob','gender','qualification','joining_date','salary','signature'
                  ,'created_by','created_date','modified_by','modified_date','branch_email'
                  ,'gender_name','role','is_active']

    def get_username(self,obj):
        return str(obj.user.username)
    
    def get_gender_name(self,obj):
        return obj.get_gender_display()
    
    def get_signature(self,obj):
        if obj.signature:
            return f"{settings.BACKEND_DOMAIN}{obj.signature.url}"  
        return None    
    
class EmployeeUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ['employee_name','address','mobile_number',
                  'qualification','salary','signature','is_active']