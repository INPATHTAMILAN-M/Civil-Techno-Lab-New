from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from account.models import City      
from account.serializers import (
                City_Manage_Serializer,
                City_Serializer )




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
        cities = City.objects.all().order_by('-id')
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
        
    def delete(self, request, id):
        data = dict()
        try:
            city = City.objects.get(id=id)            
        except City.DoesNotExist:
            data['valid'] = False
            data['error'] = "City not found"
            return Response(data, status=status.HTTP_404_NOT_FOUND)
        
        if city.created_by == request.user:   
            city.delete()
            data['deleted'] = True
        else:
            data['valid'] = False
        return Response(data)
    