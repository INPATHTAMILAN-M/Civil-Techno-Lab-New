
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User, Group

from rest_framework.generics import (
    CreateAPIView, RetrieveAPIView, 
    UpdateAPIView, ListAPIView, DestroyAPIView
)

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from account.models import Employee

from account.serializers import (
                Create_Employee_Serializer,
                Employee_List_Serializer,
                Employee_Serializer,
                Group_Serializer,
                UserSerializer,
                EmployeeUpdateSerializer
)
from payment.pagination import CustomPagination

class Manage_Employee(APIView):
    def post(self, request, *args, **kwargs):
        user_serializer = UserSerializer(data=request.data)
        empolyee_serializer = Create_Employee_Serializer(data=request.data,partial=True)
        if user_serializer.is_valid() and empolyee_serializer.is_valid():
            user_serializer = user_serializer.save()
            employee_group = Group.objects.get(name='Employee')
            user_serializer.groups.add(employee_group)       
            user_serializer.save()     
            empolyee_serializer = empolyee_serializer.save(user=user_serializer,created_by=request.user, modified_by=request.user)
            return Response({'created':True}, status=status.HTTP_201_CREATED)
        else:
            errors = dict()
            if user_serializer.errors:
                errors['user'] = user_serializer.errors
            if not empolyee_serializer.is_valid():
                errors['employee'] = empolyee_serializer.errors
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, *args,**kwargs):
        employees = Employee.objects.all().order_by('-id')
        paginator = CustomPagination()
        result_page = paginator.paginate_queryset(employees, request)
        serializer = Employee_List_Serializer(result_page, many=True)
        groups = Group.objects.filter(name__in=('Admin',"Employee"))
        groups = Group_Serializer(groups,many=True)

        return paginator.get_paginated_response(serializer.data)

    def put(self, request, id):
        employee = Employee.objects.get(id=id)
        serializer = Create_Employee_Serializer(employee, data=request.data,partial=True)
        if serializer.is_valid():
            serializer = serializer.save()
            user = User.objects.get(id=serializer.user.id)
            try:
                password = request.data['password']
                if password:                
                    user.password = make_password(password)
                else:
                    pass
            except:
                pass
            
            user.username = request.data['username']
            user.save()
               
            employee = Employee.objects.get(id=serializer.id)
            serializer = Employee_Serializer(employee)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors)

    def delete(self, request, id):
        data = dict()
        try:
            employee = Employee.objects.get(id=id)
        except Employee.DoesNotExist:
            data['valid'] = False
            data['error'] = "Employee not found"
            return Response(data, status=status.HTTP_404_NOT_FOUND)

        employee.delete()
        data['deleted'] = True
        return Response(data)
    
class EmployeeUpdateView(UpdateAPIView,RetrieveAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeUpdateSerializer
    lookup_field = 'id'

class EmployeeDeleteView(DestroyAPIView):
    queryset = Employee.objects.all()
    lookup_field = 'id'
    http_method_names = ['delete']

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()        
