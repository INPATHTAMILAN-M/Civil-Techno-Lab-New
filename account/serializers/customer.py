from rest_framework import serializers
from account.models import Customer, City, State, Country

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

class CustomerSerializer(serializers.ModelSerializer):
    city1 = CitySerializer(read_only=True)
    city2 = CitySerializer(read_only=True)
    state1 = StateSerializer(read_only=True)
    state2 = StateSerializer(read_only=True)
    country1 = CountrySerializer(read_only=True)
    country2 = CountrySerializer(read_only=True)

    city1_id = serializers.PrimaryKeyRelatedField(queryset=City.objects.all(), source='city1', write_only=True)
    city2_id = serializers.PrimaryKeyRelatedField(queryset=City.objects.all(), source='city2', write_only=True, required=False, allow_null=True)
    state1_id = serializers.PrimaryKeyRelatedField(queryset=State.objects.all(), source='state1', write_only=True)
    state2_id = serializers.PrimaryKeyRelatedField(queryset=State.objects.all(), source='state2', write_only=True, required=False, allow_null=True)
    country1_id = serializers.PrimaryKeyRelatedField(queryset=Country.objects.all(), source='country1', write_only=True)
    country2_id = serializers.PrimaryKeyRelatedField(queryset=Country.objects.all(), source='country2', write_only=True, required=False, allow_null=True)

    class Meta:
        model = Customer
        fields = '__all__'
