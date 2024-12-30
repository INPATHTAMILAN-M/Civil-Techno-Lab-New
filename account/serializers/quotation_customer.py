from rest_framework import serializers
from account.models import Customer

class CreateCustomerSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Customer
        fields = ['id','customer_name','address1','city1',
                  'state1','country1','pincode1']
        