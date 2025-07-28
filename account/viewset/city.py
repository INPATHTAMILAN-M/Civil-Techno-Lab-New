from rest_framework import viewsets, filters
from rest_framework.authentication import TokenAuthentication,BaseAuthentication
from django_filters.rest_framework import DjangoFilterBackend
from account.models import City
from account.serializers import CitySerializer
from payment.pagination import CustomPagination
from rest_framework.permissions import IsAuthenticated



class CityViewSet(viewsets.ModelViewSet):
    queryset = City.objects.all().order_by('-created_date')
    serializer_class = CitySerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    # authentication_classes = [TokenAuthentication]
    pagination_class = CustomPagination
    permission_classes = [IsAuthenticated]
    search_fields = ['name']
    ordering_fields = ['created_date', 'name']
    filterset_fields = ['created_by', 'modified_by']


    def update(self, request, *args, **kwargs):
        print("User:", request.user, "Is Authenticated:", request.user.is_authenticated)
        return super().update(request, *args, **kwargs)
