from rest_framework import serializers
from account.models import UserActivity
from django.contrib.auth.models import User, Group

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('id', 'name')


class UserSerializer(serializers.ModelSerializer):
    groups = GroupSerializer(many=True, required=False)
    class Meta:
        model = User
        fields = ('username', 'password', 'groups')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = super().create(validated_data)
        if password:
            instance.set_password(password)
            instance.save()
        return instance

class UserLogGetSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = UserActivity
        fields = '__all__'
