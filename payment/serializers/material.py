from rest_framework import serializers
from general.models import Material, Print_Format, Letter_Pad_Logo

class PrintFormatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Print_Format
        fields = '__all__'  # Include all fields or specify as needed

class LetterPadLogoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Letter_Pad_Logo
        fields = '__all__'  # Include all fields or specify as needed

class MaterialSerializer(serializers.ModelSerializer):
    print_format = PrintFormatSerializer(read_only=True)
    letter_pad_logo = LetterPadLogoSerializer(read_only=True)

    class Meta:
        model = Material
        fields = [
            'id',
            'material_name',
            'template',
            'created_by',
            'created_date',
            'modified_by',
            'modified_date',
            'print_format',
            'letter_pad_logo',
        ]

class MaterialBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Material
        fields = [
            'id',
            'material_name',
            'template',
            'created_by',
            'created_date',
            'modified_by',
            'modified_date',
            'print_format',
            'letter_pad_logo',
        ]

class MaterialCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Material
        fields = [
            'material_name',
            'template',
            'print_format',
            'letter_pad_logo',
        ]

class MaterialUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Material
        fields = [
            'material_name',
            'template',
            'print_format',
            'letter_pad_logo',
        ]

class MaterialDetailSerializer(MaterialBaseSerializer):
    print_format = PrintFormatSerializer(read_only=True)
    letter_pad_logo = LetterPadLogoSerializer(read_only=True)

class MaterialListSerializer(MaterialBaseSerializer):
    print_format = PrintFormatSerializer(read_only=True)
    letter_pad_logo = LetterPadLogoSerializer(read_only=True)
