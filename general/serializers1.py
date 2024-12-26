from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Tax,Material,Report_Template,Print_Format,Letter_Pad_Logo,Test,Expense

class Create_Tax_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Tax
        fields = ['id','tax_name', 'tax_percentage', 'tax_status']


class Tax_Serializer(serializers.ModelSerializer):
    status = serializers.SerializerMethodField()
    created_by = serializers.StringRelatedField()
    modified_by = serializers.StringRelatedField()
    class Meta:
        model = Tax
        fields = ['id','tax_name', 'tax_percentage', 'tax_status','status','created_by','created_date','modified_by','modified_date']
    
    def get_status(self,obj):
        return obj.get_tax_status_display()

class Create_Material_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Material
        fields = ['id', 'material_name','template','print_format','letter_pad_logo']

class Material_Serializer(serializers.ModelSerializer):
    created_by = serializers.StringRelatedField()
    modified_by = serializers.StringRelatedField()
    class Meta:
        model = Material
        fields = ['id', 'material_name', 'created_by', 'created_date', 'modified_by', 'modified_date','template','print_format','letter_pad_logo']

class Material_Serializer1(serializers.ModelSerializer):
    class Meta:
        model = Material
        fields = ['id', 'material_name']

class PrintFormat_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Print_Format
        fields = ['id', 'name']

class LetterPad_Logo_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Letter_Pad_Logo
        fields = ['id', 'name']

class Report_template_Serializer1(serializers.ModelSerializer):
    class Meta:
        model = Report_Template
        fields = ['id','report_template_name']

class Create_ReportTemplate_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Report_Template
        fields = ['id', 'material', 'report_template_name', 'template', 'print_format', 'letter_pad_logo']

class Report_Template_Serializer(serializers.ModelSerializer):
    material = serializers.SerializerMethodField()
    print_format = serializers.SerializerMethodField()
    letter_pad_logo = serializers.SerializerMethodField()

    class Meta:
        model = Report_Template
        fields = ['id', 'material', 'report_template_name', 'template', 'print_format', 'letter_pad_logo']

    def get_material(self, obj):
        return {'id': obj.material.id, 'name': obj.material.material_name}

    def get_print_format(self, obj):
        return {'id': obj.print_format.id, 'name': obj.print_format.name}

    def get_letter_pad_logo(self, obj):
        return {'id': obj.letter_pad_logo.id, 'name': obj.letter_pad_logo.name}

class User_Serializer(serializers.ModelSerializer):
    class Meta:
        model = User  
        fields = ['id', 'username']

class Test_Serializer1(serializers.ModelSerializer):
    class Meta:
        model = Test
        fields = ['id','test_name']

class Create_Test_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Test
        fields = ['id', 'material_name', 'test_name', 'price_per_piece']

class Test_Serializer(serializers.ModelSerializer):
    material_name = serializers.StringRelatedField()
    created_by = serializers.StringRelatedField()
    modified_by = serializers.StringRelatedField()
    material_id = serializers.SerializerMethodField()

    class Meta:
        model = Test
        fields = ['id', 'material_name','material_id', 'test_name', 'price_per_piece', 'created_by', 'created_date', 'modified_by', 'modified_date']


    def get_material_id(self,obj):
        return obj.material_name.id

class Create_Expense_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = ['id', 'expense_name']

class Expense_Serializer(serializers.ModelSerializer):
    created_by = serializers.StringRelatedField()
    modified_by = serializers.StringRelatedField()
    class Meta:
        model = Expense
        fields = ['id', 'expense_name', 'created_by', 'created_date', 'modified_by', 'modified_date']

