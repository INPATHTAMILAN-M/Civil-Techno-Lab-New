import os
from django.conf import settings
from django.utils.timezone import now
from django.db.models.functions import Substr, Cast
from django.db.models import IntegerField, Max
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
from ..models import Quotation, QuotationTax
from general.models import Tax
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

    def get_next_quotation_number(self):
        current_date = now()
        year = (
            f"{current_date.year - 1}-{str(current_date.year)[2:]}"
            if current_date.month < 4
            else f"{current_date.year}-{str(current_date.year + 1)[2:]}"
        )
        start_date = f"{current_date.year - 1}-04-01" if current_date.month < 4 else f"{current_date.year}-04-01"

        max_q = (
            Quotation.objects
            .filter(date_created__gte=start_date, quotation_number__contains=year)
            .annotate(num_part=Cast(Substr('quotation_number', 5, 3), IntegerField()))
            .aggregate(max_num=Max('num_part'))
        )

        next_number = (max_q['max_num'] or 0) + 1
        return f"QUO-{next_number}/{year}"
    
    def create_quotation_tax(self, quotation):
        """
        Fetch enabled taxes and create QuotationTax entries for the given quotation.
        """

        # Get all enabled taxes (assuming BooleanField tax_status)
        enabled_taxes = Tax.objects.filter(tax_status='E')

        # Calculate subtotal from quotation tests
        subtotal = sum(
            item.quantity * item.price_per_sample
            for item in quotation.quotation_items.all()
        )

        quotation_taxes = []
        for tax in enabled_taxes:
            tax_amount = (tax.tax_percentage / 100) * subtotal
            quotation_taxes.append(
                QuotationTax(
                    quotation=quotation,
                    tax_name=tax.tax_name,
                    tax_percentage=tax.tax_percentage,
                    enabled=True if tax.id in [1, 2] else False,
                    tax_amount=tax_amount,
                    created_by=quotation.created_by,
                    modified_by=quotation.modified_by,
                )
            )

        # Bulk insert all taxes
        if quotation_taxes:
            QuotationTax.objects.bulk_create(quotation_taxes)
    
    def perform_create(self, serializer):
        quotation_number = self.get_next_quotation_number()
        instance = serializer.save(
            created_by=self.request.user,
            quotation_number=quotation_number
        )
        self.create_quotation_tax(instance)
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
    
    