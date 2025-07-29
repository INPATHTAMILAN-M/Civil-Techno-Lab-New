from rest_framework import serializers
from account.models import Customer, City, State, Country

# Reusable minimal serializers
class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ['id', 'name']

class StateSerializer(serializers.ModelSerializer):
    class Meta:
        model = State
        fields = ['id', 'name']

class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ['id', 'name']

# ✅ Create Serializer
class CustomerCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'

# ✅ Update Serializer (same as create unless you want to make fields optional)
class CustomerUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'

# ✅ Retrieve Serializer
class CustomerRetrieveSerializer(serializers.ModelSerializer):
    city1 = CitySerializer(read_only=True)
    city2 = CitySerializer(read_only=True)
    state1 = StateSerializer(read_only=True)
    state2 = StateSerializer(read_only=True)
    country1 = CountrySerializer(read_only=True)
    country2 = CountrySerializer(read_only=True)

    class Meta:
        model = Customer
        fields = '__all__'

# ✅ List Serializer (can be simplified)
class CustomerListSerializer(serializers.ModelSerializer):
    city1 = CitySerializer(read_only=True)
    city2 = CitySerializer(read_only=True)
    state1 = StateSerializer(read_only=True)
    state2 = StateSerializer(read_only=True)
    country1 = CountrySerializer(read_only=True)
    country2 = CountrySerializer(read_only=True)

    class Meta:
        model = Customer
        fields = '__all__'