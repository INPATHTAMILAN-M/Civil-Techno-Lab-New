import qrcode
from rest_framework.generics import CreateAPIView, RetrieveAPIView, UpdateAPIView, ListAPIView
from django.conf import settings

from ..models import Quotation
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

    def perform_create(self, serializer):
        instance = serializer.save(created_by=self.request.user)
        qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
        qr_url = f'{settings.BACKEND_DOMAIN}/quotation/{instance.id}'
        qr.add_data(qr_url)
        qr.make(fit=True)
        qr_image = qr.make_image(fill_color="black", back_color="white")
        qr_image.save(f'media/quotation_qr/{instance.id}.png')
        instance.quotation_qr = f"quotation_qr/{instance.id}.png"
        instance.save()

class QuotationRetrieveView(RetrieveAPIView):
    queryset = Quotation.objects.all()
    serializer_class = QuotationRetrieveSerializer

class QuotationListView(ListAPIView):
    queryset = Quotation.objects.all()
    serializer_class = QuotationListSerializer

class QuotationUpdateView(UpdateAPIView):
    queryset = Quotation.objects.all()
    serializer_class = QuotationUpdateSerializer

    def perform_update(self, serializer):
        quotation = serializer.instance

        taxes = quotation.tax.all()
        quotation_items = quotation.quotation_items.all()
        quotation = serializer.instance

        data = {
            "taxes":taxes,
            "quotation_items":quotation_items,
            "quotation":quotation
        }

        print(quotation.customer)

        return super().perform_update(serializer)
    