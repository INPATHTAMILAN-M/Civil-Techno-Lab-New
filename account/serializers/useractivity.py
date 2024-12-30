from rest_framework import serializers
from account.models import UserActivity
from account.serializers.account import UserSerializer

class UserLogGetSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = UserActivity
        fields = '__all__'

class UserLogCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserActivity
        fields = '__all__'