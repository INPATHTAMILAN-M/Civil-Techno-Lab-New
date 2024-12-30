from rest_framework import serializers
from django.contrib.auth.models import User, Group
from account.models import Employee

class Create_Employee_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ['employee_name','address','mobile_number','email','dob','gender','qualification','joining_date','salary','signature','branch_email']

class Employee_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ['id','employee_name','address','mobile_number','email','dob','gender','qualification','joining_date','salary','branch_email']

class Employee_List_Serializer(serializers.ModelSerializer):
    created_by = serializers.StringRelatedField()
    modified_by = serializers.StringRelatedField()
    username = serializers.SerializerMethodField()
    gender_name = serializers.SerializerMethodField()
    
    class Meta:
        model = Employee
        fields = ['id','username','employee_name','address','mobile_number',
                  'email','dob','gender','qualification','joining_date','salary'
                  ,'created_by','created_date','modified_by','modified_date','branch_email'
                  ,'gender_name']

    def get_username(self,obj):
        return str(obj.user.username)
    
    def get_gender_name(self,obj):
        return obj.get_gender_display()