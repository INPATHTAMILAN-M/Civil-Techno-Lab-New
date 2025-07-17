from django_filters import rest_framework as filters
from account.models import Customer

class CustomerFilter(filters.FilterSet):
    class Meta:
        model = Customer
        fields = '__all__'