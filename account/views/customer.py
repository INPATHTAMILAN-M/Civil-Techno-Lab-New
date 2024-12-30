from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from account.models import (
                Customer,
                City,
                Country,
                State,
)
from account.serializers import (
                City_Serializer,
                Country_Serializer,
                Create_Customer_Serializer,
                Customer_Serializer,
                State_Serializer,
)


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
        customers = Customer.objects.filter(is_quatation_customer=False).order_by('-id')
        serializer = Customer_Serializer(customers, many=True)
        return Response(serializer.data)