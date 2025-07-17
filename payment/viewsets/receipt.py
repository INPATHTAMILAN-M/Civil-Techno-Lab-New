from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from rest_framework.response import Response
from rest_framework import status
from payment.pagination import CustomPagination
from django_filters.rest_framework import DjangoFilterBackend
from payment.models import Receipt
from rest_framework.response import Response
from payment.serializers import (
    ReceiptListSerializer,
    ReceiptCreateSerializer,
    ReceiptDetailSerializer,
    ReceiptUpdateSerializer,
)
from payment.filters import ReceiptFilter


class ReceiptViewSet(viewsets.ModelViewSet):
    queryset = Receipt.objects.all().order_by('-created_date')
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination
    filterset_class = ReceiptFilter
    search_fields = ['cheque_number', 'upi', 'neft', 'tds', 'payment_mode', 
                     'invoice_no__invoice_no']
    
    def get_serializer_class(self):
        if self.action == 'create':
            return ReceiptCreateSerializer
        if self.action == 'list':
            return ReceiptListSerializer
        if self.action in ['update', 'partial_update']:
            return ReceiptUpdateSerializer
        return ReceiptDetailSerializer  
    
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
        instance = serializer.save(created_by=request.user, created_date=timezone.now(), modified_by=request.user)

        serializer = ReceiptDetailSerializer(instance)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save(modified_by=request.user, modified_date=timezone.now())

        return Response(ReceiptDetailSerializer(instance).data)
