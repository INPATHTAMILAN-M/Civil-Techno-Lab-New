from rest_framework import serializers
from django.contrib.auth.models import User, Group
from .models import Customer,Employee, City, State, Country, UserActivity


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password','groups')


class Group_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'

class City_Serializer(serializers.ModelSerializer):

    created_by = serializers.StringRelatedField()
    modified_by = serializers.StringRelatedField()
    class Meta:
        model = City
        fields = '__all__'


class State_Serializer(serializers.ModelSerializer):
    class Meta:
        model = State
        fields = '__all__'


class Country_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = '__all__'

class Create_Customer_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['id','customer_name','phone_no','gstin_no','email','address1','city1','state1','country1','pincode1','contact_person1','mobile_no1','contact_person_email1','place_of_testing','address2','city2','state2','country2','pincode2','contact_person2','mobile_no2','contact_person_email2']

class Customer_Serializer(serializers.ModelSerializer):
    created_by = serializers.StringRelatedField()
    modified_by = serializers.StringRelatedField()
    city1 = serializers.StringRelatedField()
    city2 = serializers.StringRelatedField()
    state1 = serializers.StringRelatedField()
    state2 = serializers.StringRelatedField()
    country1 = serializers.StringRelatedField()
    country2 = serializers.StringRelatedField()

    class Meta:
        model = Customer
        fields = '__all__'


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
        fields = ['id','username','employee_name','address','mobile_number','email','dob','gender','qualification','joining_date','salary','created_by','created_date','modified_by','modified_date','branch_email','gender_name']



    def get_username(self,obj):
        return str(obj.user.username)
    

    def get_gender_name(self,obj):
        return obj.get_gender_display()

    


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    confirm_new_password = serializers.CharField(required=True)
    




class City_Manage_Serializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ['name',]

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'last_login']

class UserLogGetSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = UserActivity
        fields = '__all__'

class UserLogCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserActivity
        fields = '__all__'