import os
from django.conf import settings
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from django.utils.timezone import now
from django.db.models.functions import Substr, Cast
from django.db.models import IntegerField, Max
from general.models import Tax
from payment.pagination import CustomPagination
import qrcode
from ..models import Quotation, QuotationTax
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
    
    def create_quotation_tax(self, quotation):
        """
        Fetch enabled taxes and create QuotationTax entries for the given quotation.
        """

        # Get all enabled taxes (assuming BooleanField tax_status)
        enabled_taxes = Tax.objects.filter(tax_status='E')

        # Calculate subtotal from quotation tests
        subtotal = sum(
            item.quantity * item.price_per_sample
            for item in quotation.quotation_tests.all()
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

    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Generate unique quotation number
        quotation_number = self.get_next_quotation_number()

        # Pass created_by and quotation_number explicitly
        instance = serializer.save(
            created_by=self.request.user,
            quotation_number=quotation_number
        )
        self.create_quotation_tax(instance)

        # QR Code generation
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

        qr_dir = os.path.join(settings.MEDIA_ROOT, 'quotation_qr')
        os.makedirs(qr_dir, exist_ok=True)
        qr_filename = f'{instance.id}.png'
        qr_path = os.path.join(qr_dir, qr_filename)
        qr_image.save(qr_path)

        new_qr_path = f'quotation_qr/{qr_filename}'
        if instance.quotation_qr != new_qr_path:
            instance.quotation_qr = new_qr_path
            instance.save(update_fields=['quotation_qr'])

        response_serializer = QuotationRetrieveSerializer(instance)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)