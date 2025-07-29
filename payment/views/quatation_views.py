import os
from django.conf import settings
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    RetrieveAPIView,
    UpdateAPIView,
)
from rest_framework.permissions import AllowAny
import qrcode
from ..models import Quotation
from ..filters import QuotationFilter
from ..serializers import (
    QuotationCreateSerializer,
    QuotationRetrieveSerializer,
    QuotationListSerializer,
    QuotationUpdateSerializer,
)



# Create API View for Creating Quotations
class QuotationCreateView(CreateAPIView):
    queryset = Quotation.objects.all()
    serializer_class = QuotationCreateSerializer
    permission_classes = [IsAuthenticated]
    
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

class QuotationRetrieveView(RetrieveAPIView):
    queryset = Quotation.objects.all().order_by('-id')
    serializer_class = QuotationRetrieveSerializer
    authentication_classes = []  # Disable authentication
    permission_classes = [AllowAny] 

class QuotationListView(ListAPIView):
    queryset = Quotation.objects.all().order_by('-id')
    permission_classes = [IsAuthenticated]
    serializer_class = QuotationListSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = QuotationFilter
    

class QuotationUpdateView(UpdateAPIView):
    queryset = Quotation.objects.all().order_by('-id')
    permission_classes = [IsAuthenticated]
    serializer_class = QuotationUpdateSerializer
    http_method_names = ['patch']
    
    