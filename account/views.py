from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import LoginSerializer
from django.contrib.auth import authenticate, update_session_auth_hash
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status  
from .models import Customer,Employee, City, Country, State, UserActivity
from .serializers import (
                UserSerializer, Create_Customer_Serializer,Customer_Serializer,
                Create_Employee_Serializer,Employee_Serializer, Group_Serializer, 
                City_Serializer, State_Serializer, Country_Serializer, Employee_List_Serializer, 
                ChangePasswordSerializer, City_Manage_Serializer, UserLogGetSerializer, UserLogCreateSerializer )
from django.contrib.auth.models import User, Group
from django.contrib.auth.hashers import make_password, check_password
from utils.log_user_action import log_user_activity


class ChangePasswordView(APIView):
    def post(self, request, *args, **kwargs):
        user = request.user
        serializer = ChangePasswordSerializer(data=request.data)

        if serializer.is_valid():
            old_password = serializer.validated_data.get('old_password')
            new_password = serializer.validated_data.get('new_password')
            confirm_new_password = serializer.validated_data.get('confirm_new_password')

            # Check if the old password is correct
            if not user.check_password(old_password):
                return Response({'detail': 'Old password is incorrect.'}, status=status.HTTP_400_BAD_REQUEST)

            # Check if the new passwords match
            if new_password != confirm_new_password:
                return Response({'detail': 'New passwords do not match.'}, status=status.HTTP_400_BAD_REQUEST)

            # Update the user's password
            user.set_password(new_password)
            user.save()

            # Update the session to prevent logout
            update_session_auth_hash(request, user)

            return Response({'detail': 'Password changed successfully.'}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class Login_View(APIView):
    authentication_classes = ()
    permission_classes = ()

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                token, created = Token.objects.get_or_create(user=user)
                log_user_activity(user=user, action="LOGIN",
                                  ip=request.META.get('HTTP_X_FORWARDED_FOR'),details=request.META)
                if User.objects.filter(groups__name="Admin",id=user.id):
                    is_admin = True                    
                else:
                    is_admin = False

                return Response({'token': token.key,'name':str(user),'is_admin':is_admin}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class Logout(APIView):
    
    def get(self, request, format=None):
        # simply delete the token to force a login
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)
    
class Create_Customer(APIView):
    def post(self, request, *args, **kwargs):
        serializer = Create_Customer_Serializer(data=request.data)
        if serializer.is_valid():
            serializer = serializer.save(created_by=request.user, modified_by=request.user)
            customer = Customer.objects.get(id=serializer.id)
            serializer = Customer_Serializer(customer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, *args, **kwargs):
        cities = City.objects.all()
        states = State.objects.all()
        countries = Country.objects.all()
        cities = City_Serializer(cities,many=True)
        states = State_Serializer(states, many=True)
        countries = Country_Serializer(countries, many=True)

        context = {
            'city1':cities.data,
            'state1':states.data,
            'country1':countries.data,
            'city2':cities.data,
            'state2':states.data,
            'country2':countries.data,
        }

        return Response(context)


class Manage_Customer(APIView):
    def post(self, request, *args, **kwargs):
        serializer = Create_Customer_Serializer(data=request.data)
        if serializer.is_valid():
            serializer = serializer.save(created_by=request.user, modified_by=request.user)
            customer = Customer.objects.get(id=serializer.id)
            serializer = Customer_Serializer(customer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request,id, *args, **kwargs):
        customer = Customer.objects.get(id=id)
        serializer = Create_Customer_Serializer(customer)
        return Response(serializer.data)

    def put(self, request, id):
        customer = Customer.objects.get(id=id)
        serializer = Create_Customer_Serializer(customer, data=request.data,partial=True)
        if serializer.is_valid():
            serializer = serializer.save()
            customer = Customer.objects.get(id=serializer.id)
            serializer = Customer_Serializer(customer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors)

    def delete(self, request, id):
        data = dict()
        try:
            customer = Customer.objects.get(id=id)
        except Customer.DoesNotExist:
            data['valid'] = False
            data['error'] = "Customer not found"
            return Response(data, status=status.HTTP_404_NOT_FOUND)

        customer.delete()
        data['deleted'] = True
        return Response(data)

class Customer_List(APIView):
    def get(self, request, *args, **kwargs):
        customers = Customer.objects.all().order_by('-id')
        serializer = Customer_Serializer(customers, many=True)
        return Response(serializer.data)


class Manage_Employee(APIView):

    def post(self, request, *args, **kwargs):

        user_serializer = UserSerializer(data=request.data)
        empolyee_serializer = Create_Employee_Serializer(data=request.data,partial=True)
        if user_serializer.is_valid() and empolyee_serializer.is_valid():
            user_serializer = user_serializer.save()
            empolyee_serializer = empolyee_serializer.save(user=user_serializer,created_by=request.user, modified_by=request.user)
            return Response({'created':True}, status=status.HTTP_201_CREATED)
        else:
            errors = dict()
            if user_serializer.errors:
                errors['user'] = user_serializer.errors

            print(empolyee_serializer.is_valid())

            if not empolyee_serializer.is_valid():
                errors['employee'] = empolyee_serializer.errors

            return Response(errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, *args,**kwargs):
        employees = Employee.objects.all().order_by('-id')
        serializer = Employee_List_Serializer(employees, many=True)
        groups = Group.objects.filter(name__in=('Admin',"Employee"))
        groups = Group_Serializer(groups,many=True)

        return Response(serializer.data)

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



def check_cors(request):

    return render(request,'cors.html')



class Manage_City(APIView):

    def post(self, request, *args, **kwargs):
        serializer = City_Manage_Serializer(data=request.data)
        if serializer.is_valid():
            serializer = serializer.save(created_by=request.user,modified_by=request.user)
            city = City.objects.get(id=serializer.id)
            serializer = City_Serializer(city)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request, *args, **kwargs):
        cities = City.objects.all()
        serializer = City_Serializer(cities, many=True)  
        context = {
            'cities':serializer.data,
        }
        return Response(serializer.data)
    
    def put(self, request, id):    
        city  = City.objects.get(id=id)
        serializer = City_Manage_Serializer(city,data=request.data,partial=True)
        if serializer.is_valid():         
            serializer = serializer.save(modified_by=request.user)
            city = City.objects.get(id=serializer.id)
            serializer = City_Manage_Serializer(city)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors)
        
    def delete(self,request,id):
        data = dict()
        try:
            city = City.objects.get(id=id)            
        except ObjectDoesNotExist:
            data['valid'] = False
            data['error'] = "City not found"
            return Response(data,status=status.HTTP_404_NOT_FOUND)
        
        if city.created_by == request.user:   
            city.delete()
            data['deleted'] = True
        else:
            data['valid'] = False
        return Response(data)
    

class Userlogs(APIView):
    http_method_names = ['get', 'post']
    
    def get(self, request, *args, **kwargs):
        user_logs = UserActivity.objects.all()
        serializer = UserLogGetSerializer(user_logs, many=True)
        return Response(serializer.data)
        
    # def post(self, request, *args, **kwargs):
    #     serializer = UserLogCreateSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save(user=request.user)
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)