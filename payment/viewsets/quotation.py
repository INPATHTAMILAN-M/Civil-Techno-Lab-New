import os
from django.conf import settings
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
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
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Save to get instance.id (no QR yet)
        instance = serializer.save(created_by=self.request.user)

        # Generate QR code using instance.id
        qr_url = f'{settings.QR_DOMAIN}/invoice/viewQuotationPreview?id={instance.id}'
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4
        )
        qr.add_data(qr_url)
        qr.make(fit=True)
        qr_image = qr.make_image(fill_color="black", back_color="white")

        # Save QR image
        qr_dir = os.path.join(settings.MEDIA_ROOT, 'quotation_qr')
        os.makedirs(qr_dir, exist_ok=True)
        qr_filename = f'{instance.id}.png'
        qr_path = os.path.join(qr_dir, qr_filename)
        qr_image.save(qr_path)

        # Save QR path only if it changed
        new_qr_path = f'quotation_qr/{qr_filename}'
        if instance.quotation_qr != new_qr_path:
            instance.quotation_qr = new_qr_path
            instance.save(update_fields=['quotation_qr'])

        # Serialize using retrieve serializer
        response_serializer = QuotationRetrieveSerializer(instance)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)