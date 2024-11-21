from django.shortcuts import render, redirect
from rest_framework.views import APIView
from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from .models import Tax ,Material,Report_Template,Print_Format,Letter_Pad_Logo,Test,Expense
from .serializers import Tax_Serializer, Create_Tax_Serializer,Create_Material_Serializer,Material_Serializer,PrintFormat_Serializer,LetterPad_Logo_Serializer,Create_ReportTemplate_Serializer,Report_Template_Serializer ,Create_Test_Serializer,Test_Serializer,Report_template_Serializer1,Material_Serializer1,Test_Serializer1,Create_Expense_Serializer,Expense_Serializer   


class Manage_Tax(APIView):
    def post(self, request, *args, **kwargs):
        serializer = Create_Tax_Serializer(data=request.data)
        if serializer.is_valid():
            serializer = serializer.save(created_by=request.user,modified_by=request.user)
            tax = Tax.objects.get(id=serializer.id)
            serializer = Tax_Serializer(tax)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request, *args, **kwargs):
        taxes = Tax.objects.all()
        serializer = Tax_Serializer(taxes, many=True)  
        return Response(serializer.data)
    
    def put(self, request, id):    
        tax  = Tax.objects.get(id=id)
        serializer = Create_Tax_Serializer(tax,data=request.data,partial=True)
        if serializer.is_valid():         
            serializer = serializer.save()
            tax = Tax.objects.get(id=serializer.id)
            serializer = Tax_Serializer(tax)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors)
        
    def delete(self,request,id):
        data = dict()
        try:
            tax = Tax.objects.get(id=id)            
        except ObjectDoesNotExist:
            data['valid'] = False
            data['error'] = "Tax not found"
            return Response(data,status=status.HTTP_404_NOT_FOUND)
        
        if tax.created_by == request.user:   
            tax.delete()
            data['deleted'] = True
        else:
            data['valid'] = False
        return Response(data)
    

class Create_Material(APIView):

    def post(self, request, *args, **kwargs):
        serializer = Create_Material_Serializer(data=request.data)
        if serializer.is_valid():
            serializer = serializer.save(created_by=request.user, modified_by=request.user)
            material = Material.objects.get(id=serializer.id)
            serializer = Material_Serializer(material)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, *args, **kwargs):
   
        print_format = Print_Format.objects.all()
        letter_pad_logo = Letter_Pad_Logo.objects.all()
        print_format_serializer = PrintFormat_Serializer (print_format, many=True)
        letter_pad_logo_serializer = LetterPad_Logo_Serializer(letter_pad_logo, many=True)
        context = {
                   
                    'print_format': print_format_serializer.data,
                    'letter_pad_logo':letter_pad_logo_serializer.data,
                }
        return Response(context)
    
class Manage_Material(APIView):

    def get(self, request, *args, **kwargs):
        materials = Material.objects.all()
        serializer = Material_Serializer(materials, many=True)
        return Response(serializer.data)

    def put(self, request, id):
        material = Material.objects.get(id=id)
        serializer = Create_Material_Serializer(material, data=request.data,partial=True)
        if serializer.is_valid():
            serializer = serializer.save()
            material = Material.objects.get(id=serializer.id)
            serializer = Material_Serializer(material)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors)
        
    def post(self, request, *args, **kwargs):
        serializer = Create_Material_Serializer(data=request.data)
        if serializer.is_valid():
            serializer = serializer.save(created_by=request.user,modified_by=request.user)
            material = Material.objects.get(id=serializer.id)
            serializer = Material_Serializer(material)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        data = dict()
        try:
            material = Material.objects.get(id=id)
        except Material.DoesNotExist:
            data['valid'] = False
            data['error'] = "Material not found"
            return Response(data, status=status.HTTP_404_NOT_FOUND)

        if material.created_by == request.user:
            material.delete()
            data['deleted'] = True
        else:
            data['valid'] = False
        return Response(data)

class Create_Report_Template(APIView):

    def get(self, request):
        materials = Material.objects.all()
        print_format = Print_Format.objects.all()
        letter_pad_logo = Letter_Pad_Logo.objects.all()
        material_serializer = Material_Serializer1(materials, many=True)
        print_format_serializer = PrintFormat_Serializer (print_format, many=True)
        letter_pad_logo_serializer = LetterPad_Logo_Serializer(letter_pad_logo, many=True)
        context = {
                    'materials': material_serializer.data,
                    'print_format': print_format_serializer.data,
                    'letter_pad_logo':letter_pad_logo_serializer.data,
                }
        return Response(context)    

    def post(self, request, *args, **kwargs):
        serializer = Create_ReportTemplate_Serializer(data=request.data)
        if serializer.is_valid():
            serializer = serializer.save()
            report_template = Report_Template.objects.get(id=serializer.id)
            serializer = Report_Template_Serializer(report_template)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class Edit_Report_Template(APIView):

    def get(self, request,id):
        materials = Material.objects.all()
        print_format = Print_Format.objects.all()
        letter_pad_logo = Letter_Pad_Logo.objects.all()
        report_template = Report_Template.objects.all()
        material_serializer = Material_Serializer1(materials, many=True)
        print_format_serializer = PrintFormat_Serializer (print_format, many=True)
        letter_pad_logo_serializer = LetterPad_Logo_Serializer(letter_pad_logo, many=True)
        report_template_serializer = Report_template_Serializer1(report_template, many=True)
        context = {
                    'materials': material_serializer.data,
                    'print_format': print_format_serializer.data,
                    'letter_pad_logo':letter_pad_logo_serializer.data,
                    'report_template':report_template_serializer.data,
                    
                }
        return Response(context)

    def put(self, request, id):
        report_template = Report_Template.objects.get(id=id)
        serializer = Create_ReportTemplate_Serializer(report_template, data=request.data,partial=True)
        if serializer.is_valid():
            serializer = serializer.save()
            report_template = Report_Template.objects.get(id=serializer.id)
            serializer = Report_Template_Serializer(report_template)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors)

class List_Report_Template(APIView):

    def get(self, request, *args, **kwargs):
        report_templates = Report_Template.objects.all()
        serializer = Report_Template_Serializer(report_templates, many=True)
        return Response(serializer.data)

class Delete_Report_Template(APIView):

    def delete(self, request, id):
        data = dict()
        try:
            report_template = Report_Template.objects.get(id=id)
        except Report_Template.DoesNotExist:
            data['valid'] = False
            data['error'] = "Report Template not found"
            return Response(data, status=status.HTTP_404_NOT_FOUND)

        report_template.delete()
        data['deleted'] = True
        return Response(data)

class Create_Test(APIView):
    
    def get(self, request):
        materials = Material.objects.all()
        material_serializer = Material_Serializer1(materials, many=True)
        context = {
                    'materials': material_serializer.data,
                }
        return Response(context)

    def post(self, request, *args, **kwargs):
        serializer = Create_Test_Serializer(data=request.data)
        if serializer.is_valid():
            serializer = serializer.save(created_by=request.user, modified_by=request.user)
            test = Test.objects.get(id=serializer.id)
            serializer = Test_Serializer(test)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class List_Test(APIView):
    def get(self, request, *args, **kwargs):
        tests = Test.objects.all()
        serializer = Test_Serializer(tests, many=True)
        return Response(serializer.data)

class Edit_Test(APIView):

    def get(self, request,id):
        materials = Material.objects.all()
        tests = Test.objects.all()
        material_serializer = Material_Serializer1(materials, many=True)
        test_serializer = Test_Serializer1(tests, many=True)
        context = {
                    'materials': material_serializer.data,
                    'tests': test_serializer.data,
                }
        return Response(context)
        
    def put(self, request, id):
        test = Test.objects.get(id=id)
        serializer = Create_Test_Serializer(test, data=request.data,partial=True)
        if serializer.is_valid():
            serializer = serializer.save(modified_by=request.user)
            test = Test.objects.get(id=serializer.id)
            serializer = Test_Serializer(test)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors)

class Delete_Test(APIView):
    def delete(self, request, id):
        data = dict()
        try:
            test = Test.objects.get(id=id)
        except Test.DoesNotExist:
            data['valid'] = False
            data['error'] = "Test not found"
            return Response(data, status=status.HTTP_404_NOT_FOUND)
        test.delete()
        data['deleted'] = True
        return Response(data)     

class Manage_Expense(APIView):
    def post(self, request, *args, **kwargs):
        serializer = Create_Expense_Serializer(data=request.data)
        if serializer.is_valid():
            serializer = serializer.save(created_by=request.user, modified_by=request.user)
            expense = Expense.objects.get(id=serializer.id)
            serializer = Expense_Serializer(expense)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, *args, **kwargs):
        expenses = Expense.objects.all()
        serializer = Expense_Serializer(expenses, many=True)
        return Response(serializer.data)

    def put(self, request, id):
        expense = Expense.objects.get(id=id)
        serializer = Create_Expense_Serializer(expense, data=request.data,partial=True)
        if serializer.is_valid():
            serializer = serializer.save()
            expense = Expense.objects.get(id=serializer.id)
            serializer = Expense_Serializer(expense)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors)

    def delete(self, request, id):
        data = dict()
        try:
            expense = Expense.objects.get(id=id)
        except Expense.DoesNotExist:
            data['valid'] = False
            data['error'] = "Expense not found"
            return Response(data, status=status.HTTP_404_NOT_FOUND)

        expense.delete()
        data['deleted'] = True
        return Response(data)

