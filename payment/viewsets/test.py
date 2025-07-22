from rest_framework import viewsets, filters
from django.utils import timezone
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from payment.pagination import CustomPagination
from django_filters.rest_framework import DjangoFilterBackend
from general.models import Test
from payment.serializers import (
    TestCreateSerializer,
    TestUpdateSerializer,
    TestDetailSerializer,
    TestListSerializer

)
from payment.filters import TestFilter

class TestViewSet(viewsets.ModelViewSet):
    queryset = Test.objects.all().order_by('-created_date')
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_class = TestFilter
    search_fields = ['test_name', 'material_name__material_name']  # adjust based on Material model


    def get_serializer_class(self):
        if self.action == 'create':
            return TestCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return TestUpdateSerializer
        elif self.action == 'retrieve':
            return TestDetailSerializer
        elif self.action == 'list':
            return TestListSerializer
        return TestDetailSerializer


    def list(self, request, *args, **kwargs):
        pagination_param = request.query_params.get('pagination', 'true').lower()

        queryset = self.filter_queryset(self.get_queryset())

        if pagination_param == 'false':
            MAX_RESULTS = 300
            queryset = queryset[:MAX_RESULTS]  # Hard cap to avoid excessive load
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)

        return super().list(request, *args, **kwargs)
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save(created_by=request.user, created_date=timezone.now())
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save(modified_by=request.user, modified_date=timezone.now())
        self.perform_update(serializer)
        return Response(serializer.data)
    

    
    
