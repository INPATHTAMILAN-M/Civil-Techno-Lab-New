from rest_framework import serializers
from account.models import City, State, Country


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


class City_Manage_Serializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ['name',]