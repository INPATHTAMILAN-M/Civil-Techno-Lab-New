from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
# from rest_framework.authentication import TokenAuthentication,BasicAuthentication
from django_filters.rest_framework import DjangoFilterBackend
from general.models import Material
from rest_framework.response import Response
from payment.pagination import CustomPagination
from payment.serializers import (
    MaterialListSerializer,
    MaterialCreateSerializer,
    MaterialUpdateSerializer,
    MaterialDetailSerializer,
)

class MaterialViewSet(viewsets.ModelViewSet):
    queryset = Material.objects.all().order_by('-created_date')
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    pagination_class = CustomPagination
    # authentication_classes = [TokenAuthentication,BasicAuthentication]
    permission_classes = [IsAuthenticated]
    search_fields = ['material_name']
    ordering_fields = ['created_date', 'material_name']
    filterset_fields = ['print_format', 'letter_pad_logo', 'created_by']

    def get_serializer_class(self):
        if self.action == 'list':
            return MaterialListSerializer
        elif self.action == 'create':
            return MaterialCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return MaterialUpdateSerializer
        elif self.action == 'retrieve':
            return MaterialDetailSerializer
        return super().get_serializer_class()
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(created_by=request.user)
        self.perform_create(serializer)
        return Response(serializer.data, status=201)
    

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save(modified_by=request.user)
        return Response(serializer.data)


