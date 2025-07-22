from rest_framework import serializers
from django.contrib.auth.models import User
from ..models import Material


class Create_Material_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Material
        fields = ['id', 'material_name','template','print_format','letter_pad_logo']

class Material_Serializer(serializers.ModelSerializer):
    created_by = serializers.StringRelatedField()
    modified_by = serializers.StringRelatedField()
    class Meta:
        model = Material
        fields = ['id', 'material_name', 'created_by', 'created_date', 'modified_by', 'modified_date','template','print_format','letter_pad_logo']
