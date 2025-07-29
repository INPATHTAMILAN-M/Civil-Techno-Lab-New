import os
from django.conf import settings
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from payment.pagination import CustomPagination
import qrcode
from ..models import Quotation
from ..filters import QuotationFilter
from ..serializers import (
    QuotationCreateSerializer,
    QuotationRetrieveSerializer,
    QuotationListSerializer,
    QuotationUpdateSerializer,
)

class QuotationViewSet(ModelViewSet):
    queryset = Quotation.objects.all().order_by('-id')
    filter_backends = [DjangoFilterBackend]
    filterset_class = QuotationFilter
    pagination_class = CustomPagination
    
    def get_serializer_class(self):
        if self.action == 'create':
            return QuotationCreateSerializer
        elif self.action == 'retrieve':
            return QuotationRetrieveSerializer
        elif self.action == 'list':
            return QuotationListSerializer
        elif self.action in ['update', 'partial_update']:
            return QuotationUpdateSerializer
        return QuotationListSerializer  # default
    
    def get_permissions(self):
        if self.action == 'retrieve':
            return [AllowAny()]
        return [IsAuthenticated()]
    
    def perform_create(self, serializer):
        instance = serializer.save(created_by=self.request.user)
        qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
        qr_url = f'{settings.QR_DOMAIN}/invoice/viewQuotationPreview?id={instance.id}'
        qr.add_data(qr_url)
        qr.make(fit=True)
        qr_image = qr.make_image(fill_color="black", back_color="white")
        qr_dir = os.path.join(settings.MEDIA_ROOT, 'quotation_qr')
        os.makedirs(qr_dir, exist_ok=True)

        # Save the QR image
        qr_path = os.path.join(qr_dir, f'{instance.id}.png')
        qr_image.save(qr_path)
        instance.quotation_qr = f"quotation_qr/{instance.id}.png"
        instance.save()