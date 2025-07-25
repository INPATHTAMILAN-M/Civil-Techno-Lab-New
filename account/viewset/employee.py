from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from account.models import Employee
from account.serializers import Create_Employee_Serializer, Employee_Serializer, Employee_List_Serializer, EmployeeUpdateSerializer
from account.filters.employee_filter import EmployeeFilter
from account.serializers import UserSerializer
from payment.pagination import CustomPagination
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.contrib.auth.models import Group, User
from django.contrib.auth.hashers import make_password
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.permissions import IsAuthenticated

class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = Employee_Serializer
    pagination_class = CustomPagination
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = EmployeeFilter

    def get_queryset(self):
        return self.queryset.order_by('-created_date')

    def get_serializer_class(self):
        if self.action == 'create':
            return Create_Employee_Serializer
        elif self.action in ['update', 'partial_update']:
            return EmployeeUpdateSerializer
        elif self.action == 'list':
            return Employee_List_Serializer
        return Employee_Serializer

    def create(self, request, *args, **kwargs):
        # First, validate and save User
        user_serializer = UserSerializer(data=request.data)
        employee_serializer = Create_Employee_Serializer(data=request.data, partial=True)

        if user_serializer.is_valid() and employee_serializer.is_valid():
            user = user_serializer.save()
            
            # Add to group
            try:
                employee_group = Group.objects.get(name='Employee')
                user.groups.add(employee_group)
            except Group.DoesNotExist:
                return Response({"error": "Employee group does not exist."}, status=status.HTTP_400_BAD_REQUEST)
            
            user.save()

            # Save employee with user and request user context
            employee = employee_serializer.save(
                user=user,
                created_by=request.user,
                modified_by=request.user
            )

            return Response({'created': True}, status=status.HTTP_201_CREATED)

        errors = {}
        if user_serializer.errors:
            errors['user'] = user_serializer.errors
        if employee_serializer.errors:
            errors['employee'] = employee_serializer.errors

        return Response(errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        employee = self.get_object()
        serializer = EmployeeUpdateSerializer(employee, data=request.data, partial=partial)

        if serializer.is_valid():
            employee = serializer.save(modified_by=request.user)
            user = employee.user

            # Update password if provided
            password = request.data.get('password', None)
            if password:
                user.password = make_password(password)

            # Update username if provided
            username = request.data.get('username')
            if username:
                user.username = username

            user.save()

            return Response(Employee_Serializer(employee).data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_active = False
        instance.save()
        return Response({'deleted': True}, status=status.HTTP_200_OK)
